#!/usr/bin/env python3
"""tw.py: spend fewer tokens on the same result. Standard library only, Python 3.9+.

Commands
  changed <paths...>      skip a re-read: report which files changed since the last snapshot, print only the diff
  score [transcript]      rank the token sinks in a Claude Code transcript (JSONL) and name the fix
  repeats <transcripts..> find command sequences repeated across sessions: script candidates
  skill <dir>             token cost of a skill or plugin: what loads always, on trigger, on demand
  estimate <paths...>     rough token count of files (chars / 4)
  catalog <args...>       the whole skill catalog: forwards to tokenwright-catalog's tidy.py (lint, conflicts, park...)
  hook <pre|post>         hook entry point (reads the hook JSON on stdin); off unless TOKENWRIGHT_HOOKS is set

Token counts are estimates (about 4 characters per token for English and code). Use them to rank, not to bill.
"""
import argparse
import difflib
import hashlib
import json
import os
import re
import subprocess
import sys
from collections import Counter, defaultdict
from pathlib import Path

VERSION = "0.2.3"
CHARS_PER_TOKEN = 4
BIG_FILE_LINES = 400        # a whole read of a file this long, used for a few lines, is a sink
BIG_OUTPUT_CHARS = 20000    # a tool result this long is a sink unless it was the point
SNAP_DIR_DEFAULT = ".tokenwright/snapshots"
SNAP_MAX_BYTES = 2_000_000
IMAGE_TOKENS = 1600         # a full-size image costs roughly this much; resize to cut it
IMAGE_EXT = (".png", ".jpg", ".jpeg", ".gif", ".webp", ".bmp")


def tokens(n_chars):
    return (n_chars + CHARS_PER_TOKEN - 1) // CHARS_PER_TOKEN


def out(text):
    sys.stdout.write(text.rstrip("\n") + "\n")


# ---------------------------------------------------------------- changed

def _snap_root(arg):
    return Path(arg or os.environ.get("TOKENWRIGHT_SNAPSHOTS") or SNAP_DIR_DEFAULT)


def _snap_name(path):
    return hashlib.sha1(str(Path(path).resolve()).lower().encode("utf-8")).hexdigest()[:16]


def _line_count(data):
    return data.count(b"\n") + (1 if data and not data.endswith(b"\n") else 0)


def cmd_changed(a):
    root = _snap_root(a.snapshots)
    root.mkdir(parents=True, exist_ok=True)
    unchanged = 0
    for p in a.paths:
        path = Path(p)
        meta_f = root / (_snap_name(path) + ".json")
        body_f = root / (_snap_name(path) + ".snap")
        if not path.is_file():
            out("missing   %s" % p)
            continue
        st = path.stat()
        old = json.loads(meta_f.read_text(encoding="utf-8")) if meta_f.exists() else None
        if old and old["size"] == st.st_size and old["mtime"] == st.st_mtime_ns:
            out("unchanged %s" % p)
            unchanged += 1
            continue
        data = path.read_bytes()
        digest = hashlib.sha256(data).hexdigest()
        if old and old["sha256"] == digest:
            out("unchanged %s (touched, same content)" % p)
            unchanged += 1
        elif not old:
            out("new       %s (%d lines, ~%d tokens): no snapshot yet; read it once" %
                (p, _line_count(data), tokens(len(data))))
        else:
            prev = body_f.read_bytes() if body_f.exists() else None
            if prev is None or b"\0" in data[:4096]:
                out("changed   %s (binary or no stored copy; read it)" % p)
            else:
                diff = list(difflib.unified_diff(
                    prev.decode("utf-8", "replace").splitlines(),
                    data.decode("utf-8", "replace").splitlines(),
                    "before", "after", n=a.context, lineterm=""))
                changed = sum(1 for d in diff if d[:1] in "+-" and d[:3] not in ("+++", "---"))
                out("changed   %s (%d changed lines; diff ~%d tokens vs whole file ~%d)" %
                    (p, changed, tokens(sum(len(d) + 1 for d in diff)), tokens(len(data))))
                if not a.quiet:
                    for d in diff[2:]:
                        out("  " + d)
        if not a.dry_run:
            meta_f.write_text(json.dumps({"path": str(path), "size": st.st_size,
                                          "mtime": st.st_mtime_ns, "sha256": digest}), encoding="utf-8")
            if len(data) <= SNAP_MAX_BYTES:
                body_f.write_bytes(data)
    if a.paths and unchanged == len(a.paths):
        out("all unchanged: skip the re-read")
    return 0


# ---------------------------------------------------------------- transcripts

def _content_text(c):
    if isinstance(c, str):
        return c
    if isinstance(c, list):
        return "".join(_content_text(x.get("text") or x.get("content") or "") if isinstance(x, dict) else str(x)
                       for x in c)
    return "" if c is None else str(c)


def load_events(path):
    """Yield (kind, data) in order: ('use', {id,name,input}), ('result', {id,text,error}), ('usage', usage)."""
    seen_req = set()
    with open(path, encoding="utf-8", errors="replace") as f:
        for line in f:
            try:
                rec = json.loads(line)
            except ValueError:
                continue
            msg = rec.get("message") if isinstance(rec, dict) else None
            if not isinstance(msg, dict):
                continue
            req = rec.get("requestId") or msg.get("id")
            if msg.get("usage") and rec.get("type") == "assistant" and (not req or req not in seen_req):
                seen_req.add(req)   # one response spans several lines that repeat its usage
                yield "usage", msg["usage"]
            content = msg.get("content")
            if not isinstance(content, list):
                continue
            for c in content:
                if not isinstance(c, dict):
                    continue
                if c.get("type") == "tool_use":
                    yield "use", {"id": c.get("id"), "name": c.get("name", "?"), "input": c.get("input") or {}}
                elif c.get("type") == "tool_result":
                    yield "result", {"id": c.get("tool_use_id"), "text": _content_text(c.get("content")),
                                     "error": bool(c.get("is_error"))}


def latest_transcript():
    root = Path.home() / ".claude" / "projects"
    files = list(root.glob("*/*.jsonl"))
    if not files:
        sys.exit("no transcripts under %s" % root)
    return max(files, key=lambda p: p.stat().st_mtime)


def _norm_path(p):
    return str(p).replace("\\", "/").lower() if p else ""


def _bash_reads_whole(cmd):
    m = re.match(r"^\s*(?:cd [^&;]+(?:&&|;)\s*)?(cat|type|Get-Content)\s+(\"[^\"]+\"|\S+)\s*$", cmd or "")
    return m.group(2).strip('"') if m else None


def score(path):
    uses, sinks = {}, []
    usage = Counter()
    reads = defaultdict(list)     # path -> [turn index of read]
    edits = defaultdict(list)     # path -> [turn index of edit]
    last_fail = {}
    n = turn = 0
    at_turn = {}
    for kind, d in load_events(path):
        if kind == "usage":
            turn += 1
            for k in ("input_tokens", "output_tokens", "cache_read_input_tokens", "cache_creation_input_tokens"):
                usage[k] += int(d.get(k) or 0)
            usage["turns"] += 1
            continue
        if kind == "use":
            n += 1
            uses[d["id"]] = (n, d)
            at_turn[n] = turn
            continue
        if d["id"] not in uses:
            continue
        i, u = uses[d["id"]]
        name, inp, text = u["name"], u["input"], d["text"]
        size = len(text)
        if name == "Read" and str(inp.get("file_path") or "").lower().endswith(IMAGE_EXT):
            size = IMAGE_TOKENS * CHARS_PER_TOKEN
        fp = _norm_path(inp.get("file_path") or inp.get("path") or inp.get("notebook_path"))
        if name in ("Edit", "Write", "MultiEdit", "NotebookEdit") and fp:
            edits[fp].append(i)
        if name == "Read" and fp and not d["error"]:
            lines = text.count("\n") + 1
            prev = reads[fp]
            # a second whole read is counted once, as a repeat read
            if lines >= BIG_FILE_LINES and not prev and not inp.get("offset") and not inp.get("limit"):
                sinks.append(("whole-read", tokens(size), i, "Read %s whole (%d lines)" % (fp, lines),
                              "search first (Grep -n with -C), then Read offset/limit; or readwright outline"))
            if prev:
                edited_between = any(prev[-1] < e < i for e in edits[fp])
                own_edit = edited_between and not inp.get("offset")
                label = "re-read after own edit" if own_edit else "repeat read"
                fix = ("trust the Edit result; re-read only the changed range" if own_edit
                       else "keep the facts from the first read, or `tw.py changed` to skip unchanged files")
                sinks.append((label, tokens(size), i, "Read %s again (%d reads)" % (fp, len(prev) + 1), fix))
            reads[fp].append(i)
        whole = _bash_reads_whole(inp.get("command", "")) if name in ("Bash", "PowerShell") else None
        if whole:
            sinks.append(("shell-cat", tokens(size), i, "%s printed %s whole" % (name, whole),
                          "grep -n / sed -n 'a,bp' / head; or the Read tool with a range"))
        elif size >= BIG_OUTPUT_CHARS and name != "Read":
            what = (inp.get("command") or inp.get("pattern") or inp.get("url") or inp.get("query") or "")[:70]
            sinks.append(("big-output", tokens(size), i, "%s output %d chars: %s" % (name, size, what),
                          "trim at the source: head, --stat, -q, Grep head_limit, files_with_matches; "
                          "or a subagent/local-delegate that returns only the answer"))
        key = (name, json.dumps(inp, sort_keys=True)[:300])
        if d["error"]:
            if key in last_fail:
                sinks.append(("retry", tokens(size + len(key[1])), i, "%s failed again with the same input" % name,
                              "read the error and change the call; never resend it unchanged"))
            last_fail[key] = i
    # a sink is paid again as cache read on every later turn until compaction or /clear
    sinks = [s + (s[1] * max(0, turn - at_turn.get(s[2], turn)),) for s in sinks]
    return sinks, usage, n


def cmd_score(a):
    path = Path(a.transcript) if a.transcript else latest_transcript()
    sinks, usage, n = score(path)
    by_kind = Counter()
    for k, t, *_ in sinks:
        by_kind[k] += t
    total_waste = sum(by_kind.values())
    carried = sum(s[5] for s in sinks)
    if a.json:
        out(json.dumps({"transcript": str(path), "tool_calls": n, "usage": usage, "waste_by_kind": by_kind,
                        "carried_cache_read_tokens": carried,
                        "sinks": [dict(zip(("kind", "tokens", "call", "what", "fix", "carried"), s)) for s in
                                  sorted(sinks, key=lambda s: -s[1])[:a.top]]}, indent=1))
        return 0
    out("transcript %s" % path)
    if usage:
        out("turns %d, tool calls %d; input %d, cache read %d, cache write %d, output %d tokens" % (
            usage["turns"], n, usage["input_tokens"], usage["cache_read_input_tokens"],
            usage["cache_creation_input_tokens"], usage["output_tokens"]))
    if not sinks:
        out("no sinks found")
        return 0
    out("estimated avoidable ~%d tokens entered context; carried on later turns as ~%d cache-read tokens "
        "(billed at about a tenth of input)" % (total_waste, carried))
    for k, t in by_kind.most_common():
        out("  %-22s ~%d" % (k, t))
    out("top sinks:")
    for k, t, i, what, fix, _c in sorted(sinks, key=lambda s: -s[5])[:a.top]:
        out("  ~%6d  #%-4d %-22s %s\n          fix: %s" % (t, i, k, what, fix))
    return 0


# ---------------------------------------------------------------- repeats

def _norm_cmd(cmd):
    cmd = re.sub(r"^\s*cd\s+(\"[^\"]*\"|\S+)\s*(&&|;)\s*", "", cmd or "")
    cmd = re.sub(r"\"[^\"]*\"|'[^']*'", "<s>", cmd)
    cmd = re.sub(r"\d+", "<n>", cmd)
    cmd = re.sub(r"[A-Za-z]:[\\/]\S+|/\S+", "<path>", cmd)
    return " ".join(cmd.split())[:120]


def cmd_repeats(a):
    files = [Path(p) for p in a.transcripts] or sorted(
        (Path.home() / ".claude" / "projects").glob("*/*.jsonl"), key=lambda p: p.stat().st_mtime)[-a.last:]
    seen = Counter()
    where = defaultdict(set)
    for f in files:
        cmds = [_norm_cmd(d["input"].get("command")) for k, d in load_events(f)
                if k == "use" and d["name"] in ("Bash", "PowerShell") and d["input"].get("command")]
        grams = set()
        for size in range(a.min_len, a.max_len + 1):
            for j in range(len(cmds) - size + 1):
                g = tuple(cmds[j:j + size])
                if len(set(g)) == len(g):
                    grams.add(g)
        for g in grams:
            seen[g] += 1
            where[g].add(f.name)
    hits = [(g, c) for g, c in seen.items() if c >= a.min_sessions]
    # keep the longest sequences; drop ones contained in a longer hit with the same count
    hits.sort(key=lambda x: (-x[1], -len(x[0])))
    kept = []
    for g, c in hits:
        s = " \n ".join(g)
        if any(c == c2 and s in " \n ".join(g2) for g2, c2 in kept):
            continue
        kept.append((g, c))
    out("%d transcripts scanned; %d sequences repeat in >= %d sessions" % (len(files), len(kept), a.min_sessions))
    for g, c in kept[:a.top]:
        out("\n%d sessions, %d steps -> script candidate (see tokenwright-script):" % (c, len(g)))
        for cmd in g:
            out("    " + cmd)
    return 0


# ---------------------------------------------------------------- skill

def _frontmatter(text):
    if not text.startswith("---"):
        return {}, text
    end = text.find("\n---", 3)
    head, body = text[3:end], text[end + 4:]
    fm, key = {}, None
    for line in head.splitlines():
        m = re.match(r"^([A-Za-z_-]+):\s*(.*)$", line)
        if m:
            key = m.group(1)
            fm[key] = m.group(2).strip().strip("'\"")
        elif key and line.startswith((" ", "\t")):
            fm[key] = (fm[key] + " " + line.strip()).strip()
    return fm, body


def skill_report(sdir):
    sdir = Path(sdir)
    skill_md = sdir / "SKILL.md"
    text = skill_md.read_text(encoding="utf-8", errors="replace")
    fm, body = _frontmatter(text)
    desc = fm.get("description", "")
    findings = []
    body_lines = body.count("\n")
    others = [p for p in sdir.rglob("*") if p.is_file() and p != skill_md and "__pycache__" not in p.parts
              and "evals" not in p.relative_to(sdir).parts and p.suffix in (".md", ".txt", ".json") and p.name not in ("CHANGELOG.md", "LEARNINGS.md",
                                                                            "RESEARCH.md", "TESTS.md",
                                                                            "MAINTENANCE.md", "evergreen.json")]
    if len(desc) > 1024:
        findings.append((tokens(len(desc) - 600), "description is %d chars (limit 1024 on some hosts); "
                         "it loads in every session: keep triggers, drop explanation" % len(desc)))
    elif len(desc) > 600:
        findings.append((tokens(len(desc) - 600), "description is %d chars; every session pays for it. "
                         "Aim near 300-600: what it does plus trigger phrases" % len(desc)))
    if body_lines > 500:
        findings.append((tokens(len(body)) // 2, "SKILL.md body is %d lines; move procedures and tables to "
                         "references/ loaded on demand (aim under 200-500)" % body_lines))
    code_blocks = re.findall(r"```[^\n]*\n(.*?)```", body, re.S)
    long_code = [c for c in code_blocks if c.count("\n") >= 25]
    if long_code:
        findings.append((tokens(sum(len(c) for c in long_code)), "%d code block(s) of 25+ lines in SKILL.md: "
                         "ship them as scripts the agent runs instead of text it reads" % len(long_code)))
    steps = len(re.findall(r"^\s*\d+\.\s", body, re.M))
    if steps >= 15 and not (sdir / "scripts").exists():
        findings.append((tokens(len(body)) // 4, "%d numbered steps and no scripts/: a fixed procedure this long "
                         "is a script candidate (tokenwright-script)" % steps))
    # a file is findable if SKILL.md names it, or an index SKILL.md names does
    names = re.compile(r"[\w./-]+\.(?:md|py|json|txt|sh|ps1)")
    named = {Path(x).name for x in names.findall(body)}
    for p in others:
        if p.suffix == ".md" and p.name in named:
            named |= {Path(x).name for x in names.findall(p.read_text(encoding="utf-8", errors="replace"))}
    for p in others:
        rel = p.relative_to(sdir).as_posix()
        if p.name not in named and p.stat().st_size > 2000:
            findings.append((0, "%s (~%d tokens) is never named in SKILL.md, so the agent cannot find it on "
                             "demand: link it with when to read it, or delete it" % (rel, tokens(p.stat().st_size))))
    return {"skill": fm.get("name", sdir.name), "always_tokens": tokens(len(desc) + len(fm.get("name", ""))),
            "trigger_tokens": tokens(len(text)),
            "on_demand_tokens": tokens(sum(p.stat().st_size for p in others)), "findings": findings}


def cmd_skill(a):
    root = Path(a.dir)
    dirs = [root] if (root / "SKILL.md").exists() else sorted(p.parent for p in root.rglob("SKILL.md")
                                                                         if "evals" not in p.relative_to(root).parts)
    if not dirs:
        sys.exit("no SKILL.md under %s" % root)
    reps = [skill_report(d) for d in dirs]
    if a.json:
        out(json.dumps(reps, indent=1))
        return 0
    out("%-28s %8s %9s %10s" % ("skill", "always", "on-trigger", "on-demand"))
    for r in reps:
        out("%-28s %8d %9d %10d" % (r["skill"][:28], r["always_tokens"], r["trigger_tokens"], r["on_demand_tokens"]))
    out("always = name + description, paid by every session where the skill is listed")
    allf = sorted(((t, r["skill"], m) for r in reps for t, m in r["findings"]), key=lambda x: -x[0])
    if allf:
        out("\nsavings, largest first:")
        for t, s, m in allf:
            out("  ~%5d  %s: %s" % (t, s, m))
    else:
        out("\nno obvious savings")
    return 0


# ---------------------------------------------------------------- estimate

def cmd_estimate(a):
    total = 0
    for p in a.paths:
        for f in ([Path(p)] if Path(p).is_file() else [x for x in Path(p).rglob("*") if x.is_file()]):
            n = f.stat().st_size
            total += n
            if not a.total_only:
                out("%8d  %s" % (tokens(n), f))
    out("%8d  total (~tokens)" % tokens(total))
    return 0


# ---------------------------------------------------------------- hook

def cmd_hook(a):
    mode = os.environ.get("TOKENWRIGHT_HOOKS", "").lower()
    if mode not in ("warn", "block", "1", "on"):
        return 0
    try:
        ev = json.load(sys.stdin)
    except ValueError:
        return 0
    name, inp = ev.get("tool_name", ""), ev.get("tool_input") or {}
    msg = None
    if a.when == "pre" and name == "Read" and not inp.get("offset") and not inp.get("limit"):
        fp = inp.get("file_path", "")
        try:
            size = os.path.getsize(fp)
        except OSError:
            size = 0
        if size > BIG_FILE_LINES * 60:
            msg = ("tokenwright: %s is ~%d tokens. If you need a few lines, Grep -n for them and Read with "
                   "offset/limit instead." % (fp, tokens(size)))
            if mode == "block":
                json.dump({"hookSpecificOutput": {"hookEventName": "PreToolUse", "permissionDecision": "deny",
                                                  "permissionDecisionReason": msg}}, sys.stdout)
                return 0
    elif a.when == "post":
        resp = ev.get("tool_response")
        size = len(json.dumps(resp)) if resp is not None else 0
        if size >= BIG_OUTPUT_CHARS:
            msg = ("tokenwright: that %s output was ~%d tokens. Next time trim at the source (head, --stat, -q, "
                   "head_limit) or hand the sweep to a subagent." % (name, tokens(size)))
    if msg:
        json.dump({"hookSpecificOutput": {"hookEventName": "PreToolUse" if a.when == "pre" else "PostToolUse",
                                          "additionalContext": msg}}, sys.stdout)
    return 0


TIDY = Path(__file__).resolve().parent.parent.parent / "tokenwright-catalog" / "scripts" / "tidy.py"


def cmd_catalog(a):
    if not TIDY.is_file():
        print("tokenwright: tidy.py not found at %s" % TIDY, file=sys.stderr)
        return 2
    return subprocess.run([sys.executable, str(TIDY)] + (a.args or ["--help"])).returncode


def main(argv=None):
    p = argparse.ArgumentParser(prog="tw.py", description=__doc__.split("\n")[0])
    p.add_argument("--version", action="version", version=VERSION)
    sub = p.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("changed", help="which files changed since the last snapshot; diff only")
    s.add_argument("paths", nargs="+")
    s.add_argument("--snapshots", help="snapshot dir (default .tokenwright/snapshots or $TOKENWRIGHT_SNAPSHOTS)")
    s.add_argument("--context", type=int, default=2, help="diff context lines")
    s.add_argument("--quiet", action="store_true", help="status lines only, no diff")
    s.add_argument("--dry-run", action="store_true", help="compare but do not update the snapshot")
    s.set_defaults(fn=cmd_changed)
    s = sub.add_parser("score", help="rank token sinks in a transcript")
    s.add_argument("transcript", nargs="?", help="JSONL path (default: newest under ~/.claude/projects)")
    s.add_argument("--top", type=int, default=10)
    s.add_argument("--json", action="store_true")
    s.set_defaults(fn=cmd_score)
    s = sub.add_parser("repeats", help="command sequences repeated across sessions")
    s.add_argument("transcripts", nargs="*")
    s.add_argument("--last", type=int, default=30, help="with no paths, scan the newest N transcripts")
    s.add_argument("--min-len", type=int, default=3)
    s.add_argument("--max-len", type=int, default=6)
    s.add_argument("--min-sessions", type=int, default=3)
    s.add_argument("--top", type=int, default=8)
    s.set_defaults(fn=cmd_repeats)
    s = sub.add_parser("skill", help="token cost of a skill or plugin")
    s.add_argument("dir")
    s.add_argument("--json", action="store_true")
    s.set_defaults(fn=cmd_skill)
    s = sub.add_parser("estimate", help="rough token count of files")
    s.add_argument("paths", nargs="+")
    s.add_argument("--total-only", action="store_true")
    s.set_defaults(fn=cmd_estimate)
    s = sub.add_parser("catalog", help="skill catalog commands (tidy.py): lint, conflicts, budget, park...")
    s.add_argument("args", nargs=argparse.REMAINDER)
    s.set_defaults(fn=cmd_catalog)
    s = sub.add_parser("hook", help="hook entry point (stdin JSON)")
    s.add_argument("when", choices=("pre", "post"))
    s.set_defaults(fn=cmd_hook)
    a = p.parse_args(argv)
    return a.fn(a)


if __name__ == "__main__":
    sys.exit(main())
