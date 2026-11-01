"""Write a recorded session transcript (Claude Code JSONL) with one clear token sink.

The sink: logs/app.log (3,000 lines) read whole three times while hunting one error.
Smaller noise: a few greps, one small Read, one Edit.
Run: python make_session.py OUT.jsonl
"""
import json
import sys
import uuid

SESSION = "00000000-0000-4000-8000-0000000005c0"


def log_text():
    out = []
    for i in range(3000):
        lvl = "ERROR" if i in (1204, 2210) else "INFO"
        out.append("2026-10-31T09:%02d:%02d %s worker-%d handled job %06d in %d ms"
                   % (i // 60 % 60, i % 60, lvl, i % 7, i, 20 + i % 90))
    return "\n".join("%6d\t%s" % (n, l) for n, l in enumerate(out, 1))


def main(path):
    rows, parent, n = [], None, [0]

    def add(kind, message):
        nonlocal parent
        u = str(uuid.uuid5(uuid.NAMESPACE_URL, "score-%d" % len(rows)))
        rows.append({"type": kind, "uuid": u, "parentUuid": parent, "sessionId": SESSION,
                     "isSidechain": False, "userType": "external", "cwd": "/work/shop",
                     "timestamp": "2026-10-31T10:%02d:%02dZ" % (len(rows) // 60, len(rows) % 60),
                     "message": message})
        parent = u

    def tool(name, inp, result, cache=0):
        n[0] += 1
        add("assistant", {"role": "assistant", "id": "msg_s%d" % n[0], "type": "message",
                          "model": "claude-sonnet-5-5",
                          "content": [{"type": "tool_use", "id": "toolu_s%d" % n[0], "name": name, "input": inp}],
                          "stop_reason": "tool_use",
                          "usage": {"input_tokens": 50, "output_tokens": 60,
                                    "cache_read_input_tokens": cache, "cache_creation_input_tokens": 500}})
        add("user", {"role": "user", "content": [{"type": "tool_result", "tool_use_id": "toolu_s%d" % n[0],
                                                  "content": result}]})

    big = log_text()
    add("user", {"role": "user", "content": "The nightly job failed. Find out why and fix it."})
    tool("Grep", {"pattern": "def run_job", "path": "src"}, "src/jobs.py:41:def run_job(job):", 8000)
    tool("Read", {"file_path": "/work/shop/logs/app.log"}, big, 9000)
    tool("Read", {"file_path": "/work/shop/src/jobs.py", "offset": 30, "limit": 40},
         "\n".join("%6d\t    line %d" % (k, k) for k in range(30, 70)), 40000)
    tool("Read", {"file_path": "/work/shop/logs/app.log"}, big, 41000)
    tool("Bash", {"command": "grep -c ERROR logs/app.log"}, "2", 72000)
    tool("Read", {"file_path": "/work/shop/logs/app.log"}, big, 73000)
    tool("Edit", {"file_path": "/work/shop/src/jobs.py", "old_string": "timeout=5", "new_string": "timeout=30"},
         "The file has been updated.", 105000)
    tool("Bash", {"command": "python -m pytest -q tests/test_jobs.py"}, "4 passed in 0.31s", 106000)
    add("assistant", {"role": "assistant", "id": "msg_end", "type": "message", "model": "claude-sonnet-5-5",
                      "content": [{"type": "text", "text": "Fixed: the job timed out after 5 s; raised to 30 s."}],
                      "stop_reason": "end_turn", "usage": {"input_tokens": 50, "output_tokens": 30,
                                                           "cache_read_input_tokens": 107000}})
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        for r in rows:
            f.write(json.dumps(r) + "\n")


if __name__ == "__main__":
    main(sys.argv[1])
