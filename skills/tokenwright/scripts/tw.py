#!/usr/bin/env python3
"""tw.py: spend fewer tokens on the same result. Standard library only, Python 3.9+.

Commands
  changed <paths...>      skip a re-read: report which files changed since the last snapshot, print only the diff
  score [transcript]      rank the token sinks in a Claude Code transcript (JSONL) and name the fix
  repeats <transcripts..> find command sequences repeated across sessions: script candidates
  skill <dir>             token cost of a skill or plugin: what loads always, on trigger, on demand
  estimate <paths...>     rough token count of files (chars / 2.3)
  catalog <args...>       the whole skill catalog: forwards to tokenwright-catalog's tidy.py (lint, conflicts, park...)
  hook <pre|post>         hook entry point (reads the hook JSON on stdin); off unless TOKENWRIGHT_HOOKS is set
  note --saved N --why W --how H   record, in the transcript, why and how tokenwright was used and the tokens
                          you think it saved (cost reports such as chainwright read it; prints one word)
  meter [session]         tool output so far in a session, as counted by the hook (for a status line)

Token counts are estimates (about 4 characters per token for English and code). Use them to rank, not to bill.
"""

import os
import sys

if sys.argv[1:2] == ["hook"] and os.environ.get("TOKENWRIGHT_HOOKS", "").lower() not in ("warn", "block", "1", "on"):
    sys.exit(0)   # off by default: leave before the imports below, so an idle hook costs one bare interpreter start
import argparse
import hashlib
import json
import math
import re
from collections import Counter, defaultdict
from pathlib import Path

VERSION = "0.4.4"
CHARS_PER_TOKEN = 2.3        # measured 2026-11-16 on Opus 5.5, Fable 5.2, Sonnet 5 tool output (T-20261116-10)
BIG_FILE_LINES = 400        # a whole read of a file this long, used for a few lines, is a sink
BIG_OUTPUT_CHARS = 20000    # a tool result this long is a sink unless it was the point
POLL_RUNS = 3               # the same shell command run this often is polling
DEBUG_LOOP_ERRORS = 3       # this many failed calls in a row to one tool is a debug loop
SNAP_DIR_DEFAULT = ".tokenwright/snapshots"
SNAP_MAX_BYTES = 2_000_000
IMAGE_TOKENS = 1600         # a full-size image costs roughly this much; resize to cut it
IMAGE_EXT = (".png", ".jpg", ".jpeg", ".gif", ".webp", ".bmp")
IMAGE_PX_PER_TOKEN = 750    # an image costs about width x height / 750 tokens
IMAGE_WARN_TOKENS = 3200    # twice a full-size image: above this the pre hook suggests a smaller size
METER_STEP_TOKENS = 43000   # the hook meter speaks once per this many tokens of tool output (~100k chars)
COMPARE_MIN_CALLS = 10      # past sessions shorter than this are not compared


def tokens(n_chars):
    return int(math.ceil(round(n_chars / CHARS_PER_TOKEN, 6)))


def out(text):
    sys.stdout.write(text.rstrip("\n") + "\n")


# ---------------------------------------------------------------- images

# harvestwright: kevintngo-paper-city-skill https://github.com/kevintngo/paper-city-skill tier - 2026-11-28
def image_size(path):
    """(width, height) read from a PNG, JPEG, GIF, WebP or BMP header, or None when it cannot be parsed."""
    le = lambda b: int.from_bytes(b, "little")
    be = lambda b: int.from_bytes(b, "big")
    try:
        with open(path, "rb") as f:
            h = f.read(32)
            if h[:8] == bytes.fromhex("89504e470d0a1a0a") and h[12:16] == b"IHDR":
                w, ht = be(h[16:20]), be(h[20:24])
            elif h[:6] in (b"GIF87a", b"GIF89a"):
                w, ht = le(h[6:8]), le(h[8:10])
            elif h[:2] == b"BM" and len(h) >= 26:
                w, ht = le(h[18:22]), abs(int.from_bytes(h[22:26], "little", signed=True))
            elif h[:4] == b"RIFF" and h[8:12] == b"WEBP" and len(h) >= 30:
                kind = h[12:16]
                if kind == b"VP8 " and h[23:26] == bytes.fromhex("9d012a"):
                    w, ht = le(h[26:28]) & 0x3FFF, le(h[28:30]) & 0x3FFF
                elif kind == b"VP8L" and h[20] == 0x2F:
                    w, ht = (le(h[21:25]) & 0x3FFF) + 1, ((le(h[21:25]) >> 14) & 0x3FFF) + 1
                elif kind == b"VP8X":
                    w, ht = le(h[24:27]) + 1, le(h[27:30]) + 1
                else:
                    return None
            elif h[:2] == bytes.fromhex("ffd8"):
                f.seek(2)
                while True:     # walk the segments to the frame header (SOF), which holds the size
                    b = f.read(1)
                    while b and b[0] != 0xFF:
                        b = f.read(1)
                    while b and b[0] == 0xFF:
                        b = f.read(1)
                    if not b:
                        return None
                    m = b[0]
                    if m in (0x00, 0x01, 0xD8) or 0xD0 <= m <= 0xD7:
                        continue
                    seg = f.read(2)
                    if len(seg) < 2 or m in (0xD9, 0xDA):
                        return None
                    if 0xC0 <= m <= 0xCF and m not in (0xC4, 0xC8, 0xCC):
                        d = f.read(5)
                        if len(d) < 5:
                            return None
                        w, ht = be(d[3:5]), be(d[1:3])
                        break
                    f.seek(max(be(seg) - 2, 0), 1)
            else:
                return None
    except (OSError, IndexError, ValueError):
        return None
    return (w, ht) if w > 0 and ht > 0 else None


def image_tokens(path):
    """Tokens an image costs by pixel count, or None when its header cannot be parsed. No cap is applied:
    the research notes state no size at which a host downsizes, so a very large image is overestimated."""
    wh = image_size(path)
    return int(math.ceil(wh[0] * wh[1] / IMAGE_PX_PER_TOKEN)) if wh else None


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
                diff = list(__import__("difflib").unified_diff(
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


# GitHub Copilot CLI events.jsonl (ai-docs/research/2026-11-16-other-agents-sessions.md)
_COPILOT_PREFIXES = ("tool.execution_", "session.usage_record")
# best-effort mapping; names not listed keep their own name
_COPILOT_TOOLS = {"bash": "Bash", "powershell": "PowerShell", "view": "Read", "read": "Read", "edit": "Edit",
                  "create": "Write", "write": "Write", "grep": "Grep", "rg": "Grep", "glob": "Glob", "web_fetch": "WebFetch"}


def _copilot_event(rec, seen):
    d = rec.get("data") or {}
    t = rec.get("type")
    if t == "session.usage_record":
        u = d.get("usage") or {}
        # inputTokens includes cache reads and writes (T-20261116-11); report the uncached rest like Claude's input_tokens
        rest = (u.get("inputTokens") or 0) - (u.get("cacheReadTokens") or 0) - (u.get("cacheWriteTokens") or 0)
        return "usage", {"input_tokens": max(0, rest), "output_tokens": (u.get("outputTokens") or 0)
                         + (u.get("reasoningTokens") or 0), "cache_read_input_tokens": u.get("cacheReadTokens"),
                         "cache_creation_input_tokens": u.get("cacheWriteTokens")}
    cid = d.get("toolCallId")
    if not cid or (t, cid) in seen:
        return None
    seen.add((t, cid))
    if t == "tool.execution_start":
        args = d.get("arguments") or {}
        if isinstance(args, str):
            try:
                args = json.loads(args)
            except ValueError:
                args = {"command": args}
        if isinstance(args, dict) and "path" in args and "file_path" not in args:
            args = dict(args, file_path=args["path"])
        name = d.get("toolName") or "?"
        return "use", {"id": cid, "name": _COPILOT_TOOLS.get(name, name), "input": args if isinstance(args, dict) else {}}
    if t == "tool.execution_complete":
        r = d.get("result") or {}
        text = r.get("content") if isinstance(r, dict) else r
        return "result", {"id": cid, "text": _content_text(text), "error": d.get("success") is False}
    return None


def load_events(path):
    """Yield (kind, data) in order: ('use', {id,name,input}), ('result', {id,text,error}), ('usage', usage)."""
    seen_req, seen_block = set(), set()
    with open(path, encoding="utf-8", errors="replace") as f:
        for line in f:
            try:
                rec = json.loads(line)
            except ValueError:
                continue
            if isinstance(rec, dict) and str(rec.get("type", "")).startswith(_COPILOT_PREFIXES):
                ev = _copilot_event(rec, seen_block)
                if ev:
                    yield ev
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
                kind = c.get("type")
                key = (kind, c.get("id") or c.get("tool_use_id"))
                if kind in ("tool_use", "tool_result") and key[1]:
                    if key in seen_block:   # transcripts sometimes repeat a record
                        continue
                    seen_block.add(key)
                if kind == "tool_use":
                    yield "use", {"id": c.get("id"), "name": c.get("name", "?"), "input": c.get("input") or {}}
                elif kind == "tool_result":
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
    shell_runs = Counter()        # exact shell command -> runs
    fail_streak = [None, 0]       # tool name, failed calls in a row
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
            size = int(IMAGE_TOKENS * CHARS_PER_TOKEN)
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
        cmd = (inp.get("command") or "").strip() if name in ("Bash", "PowerShell") else ""
        if cmd and not d["error"]:
            shell_runs[cmd] += 1
            if shell_runs[cmd] >= POLL_RUNS:   # about p99 of sessions (R-20261030-10)
                sinks.append(("poll", tokens(size), i, "%s ran the same command %d times: %s" % (
                    name, shell_runs[cmd], cmd[:60]), "wait with a background until-loop or Monitor "
                    "that prints only the change; or `tw.py changed`"))
        key = (name, json.dumps(inp, sort_keys=True)[:300])
        if d["error"]:
            fail_streak = [name, fail_streak[1] + 1 if fail_streak[0] == name else 1]
            if fail_streak[1] == DEBUG_LOOP_ERRORS:   # about p99 of sessions (R-20261031-1)
                sinks.append(("debug-loop", tokens(size), i, "%s failed %d times in a row" % (name, fail_streak[1]),
                              "stop and read the errors together; test the cause in isolation before the next try"))
        else:
            fail_streak = [None, 0]
        if d["error"]:
            if key in last_fail:
                sinks.append(("retry", tokens(size + len(key[1])), i, "%s failed again with the same input" % name,
                              "read the error and change the call; never resend it unchanged"))
            last_fail[key] = i
    # a sink is paid again as cache read on every later turn until compaction or /clear
    sinks = [s + (s[1] * max(0, turn - at_turn.get(s[2], turn)),) for s in sinks]
    return sinks, usage, n


LONG_CONTEXT = 400000       # requests above this context size cost more per token on long-context pricing


def context_sizes(path):
    """Context tokens sent per request (input + cache read + cache write), in order."""
    return [int(d.get("input_tokens") or 0) + int(d.get("cache_read_input_tokens") or 0)
            + int(d.get("cache_creation_input_tokens") or 0) for k, d in load_events(path) if k == "usage"]


def window_replay(sizes, window):
    """Context tokens if the session had compacted at `window`: each time the context passes it,
    it drops back to the first request's size (system prompt and tools). Rough: the summary is ignored.
    Idea from tokendoctor (https://github.com/localixai/tokendoctor, MIT), re-implemented."""
    if not sizes:
        return 0
    base, drop, total = sizes[0], 0, 0
    for c in sizes:
        if c - drop > window:
            drop = max(0, c - base)
        total += c - drop
    return total


def long_share(sizes, limit=LONG_CONTEXT):
    total = sum(sizes)
    return (100.0 * sum(c for c in sizes if c > limit) / total) if total else 0.0


def subagent_files(path):
    """Subagent transcripts of a session: <session>/subagents/**/*.jsonl beside <session>.jsonl."""
    d = path.with_suffix("") / "subagents"
    return sorted(d.rglob("*.jsonl")) if d.is_dir() else []


def cmd_score(a):
    path = Path(a.transcript) if a.transcript else latest_transcript()
    sinks, usage, n = score(path)
    sub = None
    for f in ([] if a.no_subagents else subagent_files(path)):
        s_sinks, s_usage, _n = score(f)
        sub = sub or {"count": 0, "tool_calls": 0, "usage": Counter(), "waste_tokens": 0}
        sub["count"] += 1
        sub["tool_calls"] += _n
        sub["usage"].update(s_usage)
        sub["waste_tokens"] += sum(s[1] for s in s_sinks)
        tag = "[subagent %s] " % f.stem.replace("agent-", "")[:8]
        sinks += [s[:3] + (tag + s[3],) + s[4:] for s in s_sinks]
    by_kind = Counter()
    for k, t, *_ in sinks:
        by_kind[k] += t
    total_waste = sum(by_kind.values())
    carried = sum(s[5] for s in sinks)
    sizes = context_sizes(path)
    ctx = {"context_tokens": sum(sizes), "long_context_share_pct": round(long_share(sizes), 1)}
    if a.window:
        ctx["window"] = a.window
        ctx["context_tokens_at_window"] = window_replay(sizes, a.window)
    if a.json:
        out(json.dumps({"transcript": str(path), "tool_calls": n, **ctx, "waste_per_100_calls": _rate(total_waste, n + (sub["tool_calls"] if sub else 0)), "usage": usage, "waste_by_kind": by_kind,
                        **({"subagents": sub} if sub else {}),
                        "carried_cache_read_tokens": carried,
                        "sinks": [dict(zip(("kind", "tokens", "call", "what", "fix", "carried"), s)) for s in
                                  sorted(sinks, key=lambda s: -s[1])[:a.top]]}, indent=1))
        return 0
    out("transcript %s" % path)
    if a.compare:
        compare_line(path, total_waste, n, a.compare)
    if usage:
        out("turns %d, tool calls %d; input %d, cache read %d, cache write %d, output %d tokens" % (
            usage["turns"], n, usage["input_tokens"], usage["cache_read_input_tokens"],
            usage["cache_creation_input_tokens"], usage["output_tokens"]))
    if sizes:
        out("context sent %d tokens; %.0f%% of it in requests above %dK context" % (
            ctx["context_tokens"], ctx["long_context_share_pct"], LONG_CONTEXT // 1000))
    if a.window and sizes:
        w = ctx["context_tokens_at_window"]
        out("if compacted at %dK: ~%d context tokens (%+.0f%%; rough, summary ignored)" % (
            a.window // 1000, w, 100.0 * (w - ctx["context_tokens"]) / max(1, ctx["context_tokens"])))
    if sub:
        u = sub["usage"]
        out("subagents %d: turns %d; input %d, cache read %d, cache write %d, output %d tokens (not in the line above)" % (
            sub["count"], u["turns"], u["input_tokens"], u["cache_read_input_tokens"],
            u["cache_creation_input_tokens"], u["output_tokens"]))
    if not sinks:
        out("no sinks found")
        return 0
    out("estimated avoidable ~%d tokens entered context; carried on later turns as ~%d cache-read tokens "
        "(billed at 0.1x input or less: 0.05x Opus and Sonnet 5.5, 0.025x Fable 5.x)" % (total_waste, carried))
    for k, t in by_kind.most_common():
        out("  %-22s ~%d" % (k, t))
    out("top sinks:")
    for k, t, i, what, fix, _c in sorted(sinks, key=lambda s: -s[5])[:a.top]:
        out("  ~%6d  #%-4d %-22s %s\n          fix: %s" % (t, i, k, what, fix))
    return 0


def _rate(waste, calls):
    return round(100.0 * waste / calls) if calls else 0


def compare_line(path, waste, calls, last):
    """Waste per 100 tool calls against the best and median of the newest past sessions in the same project."""
    past = sorted((p for p in path.parent.glob("*.jsonl") if p != path), key=lambda p: -p.stat().st_mtime)[:last]
    rates = []
    for p in past:
        sinks, _u, n = score(p)
        if n >= COMPARE_MIN_CALLS:
            rates.append((_rate(sum(s[1] for s in sinks), n), p.name))
    if not rates:
        out("compare: no past session in %s with %d+ tool calls" % (path.parent.name, COMPARE_MIN_CALLS))
        return
    rates.sort()
    out("compare: ~%d waste tokens per 100 calls; best of %d past sessions here ~%d (%s), median ~%d" % (
        _rate(waste, calls), len(rates), rates[0][0], rates[0][1], rates[len(rates) // 2][0]))


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
        out("\n%d sessions, %d steps -> script candidate (see tokenwright references/scripting.md):" % (c, len(g)))
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
                         "is a script candidate (tokenwright references/scripting.md)" % steps))
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
    # pictures cost by pixels, not bytes; one whose header cannot be parsed counts as a full-size image
    pics = [image_tokens(p) or IMAGE_TOKENS for p in sdir.rglob("*") if p.is_file()
            and p.suffix.lower() in IMAGE_EXT and "evals" not in p.relative_to(sdir).parts]
    return {"skill": fm.get("name", sdir.name), "always_tokens": tokens(len(desc) + len(fm.get("name", ""))),
            "trigger_tokens": tokens(len(text)), "images": len(pics), "image_tokens": sum(pics),
            "on_demand_tokens": tokens(sum(p.stat().st_size for p in others)) + sum(pics), "findings": findings}


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
    for r in reps:
        if r["images"]:
            out("%s: on-demand includes %d image(s), ~%d tokens by pixel size (width x height / %d)"
                % (r["skill"], r["images"], r["image_tokens"], IMAGE_PX_PER_TOKEN))
    # the same finding in 3+ skills folds into one line, so it cannot bury the rest (T-20261117-5)
    groups = {}
    for r in reps:
        for t, m in r["findings"]:
            groups.setdefault(re.sub(r"\d+", "N", m), []).append((t, r["skill"], m))
    allf = []
    for g in groups.values():
        if len(g) >= 3:
            names = ", ".join(s for _, s, _ in g[:4]) + (", ..." if len(g) > 4 else "")
            allf.append((sum(t for t, _, _ in g), "%d skills (%s)" % (len(g), names), g[0][2]))
        else:
            allf.extend(g)
    allf.sort(key=lambda x: -x[0])
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
        est = image_tokens(fp) if str(fp).lower().endswith(IMAGE_EXT) else None
        if est is not None:     # an image costs by its pixels; searching it or reading a range makes no sense
            if est > IMAGE_WARN_TOKENS:
                msg = ("tokenwright: %s is an image of ~%d tokens (width x height / %d). If a smaller copy "
                       "or a crop shows what you need, read that instead." % (fp, est, IMAGE_PX_PER_TOKEN))
        elif size > BIG_FILE_LINES * 60:
            msg = ("tokenwright: %s is ~%d tokens. If you need a few lines, Grep -n for them and Read with "
                   "offset/limit instead." % (fp, tokens(size)))
            if mode == "block":
                json.dump({"hookSpecificOutput": {"hookEventName": "PreToolUse", "permissionDecision": "deny",
                                                  "permissionDecisionReason": msg}}, sys.stdout)
                return 0
    elif a.when == "post":
        resp = ev.get("tool_response")
        size = len(json.dumps(resp)) if resp is not None else 0
        if name == "Bash" and isinstance(resp, dict) and "stdout" in resp:
            # Only stdout and stderr reach the model; bashEditDiff and the flags do not (T-20261116-12).
            size = len(str(resp.get("stdout") or "")) + len(str(resp.get("stderr") or ""))
        if name == "Read" and ((isinstance(resp, dict) and resp.get("type") == "image")
                               or str(inp.get("file_path") or "").lower().endswith(IMAGE_EXT)):
            size = int(IMAGE_TOKENS * CHARS_PER_TOKEN)   # base64 length is not the image's token cost
        if size >= BIG_OUTPUT_CHARS and name != "Read":
            msg = ("tokenwright: that %s output was ~%d tokens. Next time trim at the source (head, --stat, -q, "
                   "head_limit) or hand the sweep to a subagent." % (name, tokens(size)))
        # A subagent's hooks carry the parent's session_id plus agent_id; its output never reaches
        # the main context, so it stays off the main meter (T-20261116-7).
        note = None if ev.get("agent_id") else meter_add(ev.get("session_id"), name, size)
        if note:
            msg = msg + " " + note if msg else note
    if msg:
        json.dump({"hookSpecificOutput": {"hookEventName": "PreToolUse" if a.when == "pre" else "PostToolUse",
                                          "additionalContext": msg}}, sys.stdout)
    return 0


def _meter_file(session):
    root = Path(os.environ.get("TOKENWRIGHT_METER_DIR") or Path(__import__("tempfile").gettempdir()) / "tokenwright-meter")
    return root / ("%s.json" % re.sub(r"[^A-Za-z0-9_.-]", "_", str(session)))


def _meter_load(session):
    try:
        return json.loads(_meter_file(session).read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {"chars": 0, "said": 0, "by_tool": {}}


def meter_add(session, name, size):
    """Add one tool result to the session meter; return a note when it crosses the next step."""
    if not session:
        return None
    m = _meter_load(session)
    m["chars"] += size
    m["by_tool"][name] = m["by_tool"].get(name, 0) + size
    step = tokens(m["chars"]) // METER_STEP_TOKENS
    note = None
    if step > m["said"]:
        m["said"] = step
        top = max(m["by_tool"].items(), key=lambda kv: kv[1])
        note = ("tokenwright meter: ~%dk tokens of tool output so far this session (most from %s, ~%dk). "
                "Every later turn carries it until /compact or /clear." % (
                    tokens(m["chars"]) // 1000, top[0], tokens(top[1]) // 1000))
    try:
        f = _meter_file(session)
        f.parent.mkdir(parents=True, exist_ok=True)
        f.write_text(json.dumps(m), encoding="utf-8")
    except OSError:
        pass
    return note


def cmd_meter(a):
    session = a.session
    if not session:
        files = list(_meter_file("x").parent.glob("*.json"))
        if not files:
            out("tw ~0k")
            return 0
        session = max(files, key=lambda p: p.stat().st_mtime).stem
    m = _meter_load(session)
    out("tw ~%dk" % (tokens(m["chars"]) // 1000))
    return 0


def _saved(v):
    if not re.fullmatch(r"\d+(\.\d+)?[kKmM]?", v.strip()):
        raise argparse.ArgumentTypeError("--saved takes a token count such as 12000, 12k or 1.5m, not %r" % v)
    return v.strip()


def cmd_note(a):
    """Nothing to store: the command line itself sits in the transcript, where reports read it."""
    out("noted")
    return 0


TIDY = Path(__file__).resolve().parent.parent.parent / "tokenwright-catalog" / "scripts" / "tidy.py"


def cmd_catalog(a):
    if not TIDY.is_file():
        print("tokenwright: tidy.py not found at %s" % TIDY, file=sys.stderr)
        return 2
    return __import__("subprocess").run([sys.executable, str(TIDY)] + (a.args or ["--help"])).returncode


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
    s.add_argument("--no-subagents", action="store_true", help="score the main transcript only")
    s.add_argument("--compare", type=int, default=0, metavar="N",
                   help="compare with the best of the newest N past sessions in the same project")
    s.add_argument("--window", type=int, default=0, metavar="N",
                   help="replay the session as if it compacted at N context tokens")
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
    s = sub.add_parser("meter", help="tool output so far in a session, counted by the hook")
    s.add_argument("session", nargs="?", help="session id (default: the most recent)")
    s.set_defaults(fn=cmd_meter)
    s = sub.add_parser("note", help="record why/how tokenwright was used and the tokens you think it saved")
    s.add_argument("--saved", default="0", type=_saved, help="estimated tokens saved, e.g. 12000 or 12k")
    s.add_argument("--why", default="")
    s.add_argument("--how", default="")
    s.set_defaults(fn=cmd_note)
    a = p.parse_args(argv)
    return a.fn(a)


if __name__ == "__main__":
    sys.exit(main())
