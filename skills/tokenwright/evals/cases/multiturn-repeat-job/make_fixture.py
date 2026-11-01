"""Build the fixtures for multiturn-repeat-job.

make_fixture.py logs DIR   writes DIR/<date>/<service>.log for three days (the scaffold calls this)
make_fixture.py history    writes turn1.jsonl: the same two-command error summary run by hand
                           for 2026-10-30 and again for 2026-10-31
"""
import json
import random
import sys
import uuid
from pathlib import Path

HERE = Path(__file__).resolve().parent
SESSION = "00000000-0000-4000-8000-0000000e9e47"
DATES = ["2026-10-30", "2026-10-31", "2026-11-01"]
SERVICES = ["auth", "billing", "search"]
ERRORS = {"auth": ["token expired", "bad signature"], "billing": ["card declined", "ledger lock timeout"],
          "search": ["index shard missing", "query timeout"]}


def day_lines(date, svc):
    rnd = random.Random(date + svc)
    out = []
    for i in range(400):
        if rnd.random() < 0.03:
            out.append("%sT%02d:%02d:00 ERROR %s %s" % (date, i // 60 % 24, i % 60, svc, rnd.choice(ERRORS[svc])))
        else:
            out.append("%sT%02d:%02d:00 INFO %s request ok" % (date, i // 60 % 24, i % 60, svc))
    return out


def summary(date):
    per, msgs = {}, {}
    for svc in SERVICES:
        for l in day_lines(date, svc):
            p = l.split(" ", 3)
            if p[1] == "ERROR":
                per[svc] = per.get(svc, 0) + 1
                msgs[p[3]] = msgs.get(p[3], 0) + 1
    return per, msgs


def write_logs(root):
    for d in DATES:
        for svc in SERVICES:
            p = Path(root) / d / ("%s.log" % svc)
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text("\n".join(day_lines(d, svc)) + "\n", encoding="utf-8", newline="\n")


def write_history():
    rows, parent, n = [], None, [0]

    def add(kind, message):
        nonlocal parent
        u = str(uuid.uuid5(uuid.NAMESPACE_URL, "repeat-%d" % len(rows)))
        rows.append({"type": kind, "uuid": u, "parentUuid": parent, "sessionId": SESSION,
                     "isSidechain": False, "userType": "external", "cwd": ".",
                     "timestamp": "2026-11-01T09:%02d:%02dZ" % (len(rows) // 60, len(rows) % 60), "message": message})
        parent = u

    def bash(cmd, result):
        n[0] += 1
        add("assistant", {"role": "assistant", "id": "msg_j%d" % n[0], "type": "message", "model": "claude-sonnet-5-5",
                          "content": [{"type": "tool_use", "id": "toolu_j%d" % n[0], "name": "Bash",
                                       "input": {"command": cmd}}],
                          "stop_reason": "tool_use", "usage": {"input_tokens": 20, "output_tokens": 40}})
        add("user", {"role": "user", "content": [{"type": "tool_result", "tool_use_id": "toolu_j%d" % n[0],
                                                  "content": result}]})

    def say(text):
        n[0] += 1
        add("assistant", {"role": "assistant", "id": "msg_j%d" % n[0], "type": "message", "model": "claude-sonnet-5-5",
                          "content": [{"type": "text", "text": text}],
                          "stop_reason": "end_turn", "usage": {"input_tokens": 20, "output_tokens": 60}})

    for k, d in enumerate(DATES[:2]):
        per, msgs = summary(d)
        add("user", {"role": "user", "content": ("Summarise the errors in logs/%s: count per service and the most "
                                                 "common messages." if k == 0 else "Same for logs/%s please.") % d})
        bash("grep -h ' ERROR ' logs/%s/*.log | awk '{print $3}' | sort | uniq -c | sort -rn" % d,
             "\n".join("%7d %s" % (c, s) for s, c in sorted(per.items(), key=lambda x: -x[1])))
        bash("grep -h ' ERROR ' logs/%s/*.log | cut -d' ' -f4- | sort | uniq -c | sort -rn | head -5" % d,
             "\n".join("%7d %s" % (c, m) for m, c in sorted(msgs.items(), key=lambda x: -x[1])[:5]))
        say("%s: %s. Most common: %s." % (d, ", ".join("%s %d" % (s, c) for s, c in sorted(per.items())),
                                          ", ".join("%s (%d)" % (m, c) for m, c in
                                                    sorted(msgs.items(), key=lambda x: -x[1])[:2])))
    with open(HERE / "turn1.jsonl", "w", encoding="utf-8", newline="\n") as f:
        for r in rows:
            f.write(json.dumps(r) + "\n")


if __name__ == "__main__":
    if sys.argv[1] == "logs":
        write_logs(sys.argv[2])
    elif sys.argv[1] == "history":
        write_history()
    else:
        print(summary(sys.argv[1]))
