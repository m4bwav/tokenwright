"""Verify the wiki's examples against tw.py as released (tag v0.1.0).

Run from the repository root: python ai-docs/notes/2026-10-30-wiki-verify.py
Copies tw.py from the tag into a scratch folder, builds synthetic files and a
synthetic transcript there, runs each page's commands and prints one labelled
section per case. No real transcript is read.
"""
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

TAG = os.environ.get("WIKI_TAG", "v0.1.0")
REPO = Path(__file__).resolve().parents[2]
work = Path(tempfile.mkdtemp(prefix="tw-wiki-"))
tw = work / "tw.py"
tw.write_bytes(subprocess.run(["git", "-C", str(REPO), "show", TAG + ":skills/tokenwright/scripts/tw.py"],
                              capture_output=True, check=True).stdout)


def run(label, args, stdin=None, env=None):
    print("=== " + label)
    e = dict(os.environ, **(env or {}))
    e.pop("TOKENWRIGHT_SNAPSHOTS", None)
    r = subprocess.run([sys.executable, "tw.py"] + args, cwd=work, input=stdin, capture_output=True,
                       text=True, env=e)
    print((r.stdout + r.stderr).replace(str(work), "<work>").replace("\\", "/").rstrip())
    print("[exit %d]" % r.returncode)


run("version", ["--version"])

# changed
(work / "notes.md").write_text("one\ntwo\nthree\n", encoding="utf-8")
run("changed first", ["changed", "notes.md"])
run("changed again", ["changed", "notes.md"])
(work / "notes.md").write_text("one\nTWO\nthree\n", encoding="utf-8")
run("changed edited", ["changed", "notes.md"])
run("changed missing", ["changed", "nope.md"])

# estimate
(work / "big.log").write_text("x" * 39 + "\n" * 1, encoding="utf-8")
(work / "big.log").write_text(("line of log text here, forty chars long.\n") * 1000, encoding="utf-8")
run("estimate", ["estimate", "big.log", "notes.md"])
run("estimate total", ["estimate", "--total-only", "big.log", "notes.md"])

# score on a synthetic transcript
big = "\n".join("line %d" % i for i in range(500))


def line(role, content, usage=None, req=None):
    msg = {"role": role, "content": content}
    rec = {"type": role, "message": msg}
    if usage:
        msg["usage"] = usage
        rec["requestId"] = req
    return json.dumps(rec)


u = {"input_tokens": 10, "output_tokens": 20, "cache_read_input_tokens": 1000, "cache_creation_input_tokens": 100}
rows = []
for t in range(1, 6):
    calls = []
    if t in (1, 3):
        calls = [{"type": "tool_use", "id": "r%d" % t, "name": "Read", "input": {"file_path": "src/app.py"}}]
    rows.append(line("assistant", calls or [{"type": "text", "text": "ok"}], u, "q%d" % t))
    if calls:
        rows.append(line("user", [{"type": "tool_result", "tool_use_id": "r%d" % t, "content": big}]))
(work / "session.jsonl").write_text("\n".join(rows) + "\n", encoding="utf-8")
run("score", ["score", "session.jsonl"])

# repeats over three synthetic sessions
for s in range(3):
    rows = []
    for k, cmd in enumerate(["git status", "python -m unittest discover -s tests", "git push"]):
        rows.append(line("assistant", [{"type": "tool_use", "id": "b%d" % k, "name": "Bash",
                                         "input": {"command": cmd}}]))
    (work / ("s%d.jsonl" % s)).write_text("\n".join(rows) + "\n", encoding="utf-8")
run("repeats", ["repeats", "s0.jsonl", "s1.jsonl", "s2.jsonl", "--top", "1"])

# skill on a small synthetic skill
sk = work / "demo-skill"
sk.mkdir()
(sk / "SKILL.md").write_text("---\nname: demo\ndescription: Does one thing. Use on 'demo this'.\n---\n\n"
                             "# demo\n\nRead references/more.md for details.\n", encoding="utf-8")
(sk / "references").mkdir()
(sk / "references" / "more.md").write_text("details\n", encoding="utf-8")
(sk / "references" / "orphan.md").write_text("y" * 4000, encoding="utf-8")
run("skill", ["skill", "demo-skill"])

# hooks
(work / "huge.txt").write_text("z" * 30000, encoding="utf-8")
pre = json.dumps({"tool_name": "Read", "tool_input": {"file_path": "huge.txt"}})
run("hook off", ["hook", "pre"], stdin=pre)
run("hook warn", ["hook", "pre"], stdin=pre, env={"TOKENWRIGHT_HOOKS": "warn"})
run("hook block", ["hook", "pre"], stdin=pre, env={"TOKENWRIGHT_HOOKS": "block"})
run("hook on", ["hook", "pre"], stdin=pre, env={"TOKENWRIGHT_HOOKS": "on"})
post = json.dumps({"tool_name": "Bash", "tool_response": {"stdout": "a" * 25000}})
run("hook post", ["hook", "post"], stdin=post, env={"TOKENWRIGHT_HOOKS": "warn"})
