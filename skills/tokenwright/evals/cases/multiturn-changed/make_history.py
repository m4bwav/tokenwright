"""Build the fixtures for multiturn-changed: two versions of settings.py and turn1.jsonl.

Turn 1 (recorded): the agent stored a tw.py snapshot of settings.py, then read it whole.
Between turns the scaffold seeds that snapshot from settings_v1.py and puts settings_v2.py in place
(REQUEST_TIMEOUT 30 -> 45, FEATURE_0900_ENABLED False -> True).
Run: python make_history.py
"""
import json
import sys
import uuid
from pathlib import Path

HERE = Path(__file__).resolve().parent
SESSION = "00000000-0000-4000-8000-00000000c4a6"


def settings(timeout, flip):
    lines = ['"""Service settings."""', ""]
    for i in range(1500):
        if i == 700:
            lines.append("REQUEST_TIMEOUT = %d" % timeout)
        elif i == 900:
            lines.append("FEATURE_0900_ENABLED = %s" % ("True" if flip else "False"))
        else:
            lines.append("FEATURE_%04d_ENABLED = %s" % (i, "True" if i % 3 else "False"))
    return "\n".join(lines) + "\n"


def numbered(text):
    return "\n".join("%6d\t%s" % (n, l) for n, l in enumerate(text.splitlines(), 1))


def main():
    v1, v2 = settings(30, False), settings(45, True)
    (HERE / "settings_v1.py").write_text(v1, encoding="utf-8", newline="\n")
    (HERE / "settings_v2.py").write_text(v2, encoding="utf-8", newline="\n")
    rows, parent = [], None

    def add(kind, message):
        nonlocal parent
        u = str(uuid.uuid5(uuid.NAMESPACE_URL, "changed-%d" % len(rows)))
        rows.append({"type": kind, "uuid": u, "parentUuid": parent, "sessionId": SESSION,
                     "isSidechain": False, "userType": "external", "cwd": ".",
                     "timestamp": "2026-11-01T12:00:%02dZ" % len(rows), "message": message})
        parent = u

    def tool(n, name, inp, result, text=None):
        add("assistant", {"role": "assistant", "id": "msg_c%d" % n, "type": "message", "model": "claude-sonnet-5-5",
                          "content": [{"type": "tool_use", "id": "toolu_c%d" % n, "name": name, "input": inp}],
                          "stop_reason": "tool_use", "usage": {"input_tokens": 20, "output_tokens": 30}})
        add("user", {"role": "user", "content": [{"type": "tool_result", "tool_use_id": "toolu_c%d" % n,
                                                  "content": result}]})

    add("user", {"role": "user", "content": "Look over settings.py for me; I'm about to change a few things in it."})
    tool(1, "Bash", {"command": "python3 tw.py changed settings.py", "description": "Snapshot settings.py"},
         "new       settings.py (snapshot stored)")
    tool(2, "Read", {"file_path": "settings.py"}, numbered(v1))
    add("assistant", {"role": "assistant", "id": "msg_c3", "type": "message", "model": "claude-sonnet-5-5",
                      "content": [{"type": "text", "text": "settings.py holds REQUEST_TIMEOUT = 30 (line 703), "
                                   "RETRY_LIMIT is not set, and 1,499 FEATURE_nnnn_ENABLED flags. I stored a "
                                   "tw.py snapshot, so after your edit `tw.py changed settings.py` shows the diff."}],
                      "stop_reason": "end_turn", "usage": {"input_tokens": 20, "output_tokens": 40}})
    with open(HERE / "turn1.jsonl", "w", encoding="utf-8", newline="\n") as f:
        for r in rows:
            f.write(json.dumps(r) + "\n")


if __name__ == "__main__":
    if sys.argv[1:2] == ["settings"]:
        # Scaffold use: write one version straight to a path, so the versions need not be tracked.
        text = settings(30, False) if sys.argv[2] == "v1" else settings(45, True)
        Path(sys.argv[3]).write_text(text, encoding="utf-8", newline="\n")
    else:
        main()
