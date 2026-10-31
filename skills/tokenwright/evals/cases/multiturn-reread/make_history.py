"""Build the fixtures for multiturn-reread: two versions of settings.py and turn1.jsonl.

Turn 1 (recorded): the agent read settings.py whole and answered REQUEST_TIMEOUT = 30.
Between turns the scaffold puts settings_v2.py in place (timeout 45, nothing else changed).
Run: python make_history.py
"""
import json
import uuid
from pathlib import Path

HERE = Path(__file__).resolve().parent
SESSION = "00000000-0000-4000-8000-00000000bead"


def settings(timeout):
    lines = ['"""Service settings."""', ""]
    for i in range(1500):
        if i == 700:
            lines.append("REQUEST_TIMEOUT = %d" % timeout)
        elif i == 1100:
            lines.append("RETRY_LIMIT = 3")
        else:
            lines.append("FEATURE_%04d_ENABLED = %s" % (i, "True" if i % 3 else "False"))
    return "\n".join(lines) + "\n"


def numbered(text):
    return "\n".join("%6d\t%s" % (n, l) for n, l in enumerate(text.splitlines(), 1))


def main():
    v1, v2 = settings(30), settings(45)
    (HERE / "settings_v1.py").write_text(v1, encoding="utf-8", newline="\n")
    (HERE / "settings_v2.py").write_text(v2, encoding="utf-8", newline="\n")
    rows, parent = [], None

    def add(kind, message):
        nonlocal parent
        u = str(uuid.uuid5(uuid.NAMESPACE_URL, "reread-%d" % len(rows)))
        rows.append({"type": kind, "uuid": u, "parentUuid": parent, "sessionId": SESSION,
                     "isSidechain": False, "userType": "external", "cwd": ".",
                     "timestamp": "2026-10-30T12:00:%02dZ" % len(rows), "message": message})
        parent = u

    add("user", {"role": "user", "content": "What is REQUEST_TIMEOUT in settings.py?"})
    add("assistant", {"role": "assistant", "id": "msg_r1", "type": "message", "model": "claude-sonnet-5-5",
                      "content": [{"type": "tool_use", "id": "toolu_r1", "name": "Read",
                                   "input": {"file_path": "settings.py"}}],
                      "stop_reason": "tool_use", "usage": {"input_tokens": 20, "output_tokens": 30}})
    add("user", {"role": "user", "content": [{"type": "tool_result", "tool_use_id": "toolu_r1",
                                              "content": numbered(v1)}]})
    add("assistant", {"role": "assistant", "id": "msg_r2", "type": "message", "model": "claude-sonnet-5-5",
                      "content": [{"type": "text", "text": "REQUEST_TIMEOUT is 30 (line 703). "
                                   "RETRY_LIMIT is 3 (line 1103)."}],
                      "stop_reason": "end_turn", "usage": {"input_tokens": 20, "output_tokens": 20}})
    with open(HERE / "turn1.jsonl", "w", encoding="utf-8", newline="\n") as f:
        for r in rows:
            f.write(json.dumps(r) + "\n")


if __name__ == "__main__":
    main()
