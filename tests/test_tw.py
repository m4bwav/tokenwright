import io
import json
import os
import sys
import tempfile
import time
import unittest
from contextlib import redirect_stdout
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "skills" / "tokenwright" / "scripts"))
import tw  # noqa: E402


def run(*argv):
    buf = io.StringIO()
    with redirect_stdout(buf):
        tw.main(list(argv))
    return buf.getvalue()


def line(rec):
    return json.dumps(rec) + "\n"


def use(i, name, inp):
    return line({"type": "assistant", "requestId": "r%d" % i,
                 "message": {"id": "m%d" % i, "usage": {"input_tokens": 10, "output_tokens": 5,
                                                        "cache_read_input_tokens": 100},
                             "content": [{"type": "tool_use", "id": "t%d" % i, "name": name, "input": inp}]}})


def result(i, text, error=False):
    return line({"type": "user", "message": {"content": [
        {"type": "tool_result", "tool_use_id": "t%d" % i, "content": text, "is_error": error}]}})


class Changed(unittest.TestCase):
    def test_new_unchanged_changed(self):
        with tempfile.TemporaryDirectory() as d:
            f, snaps = Path(d, "a.txt"), str(Path(d, "snaps"))
            f.write_text("one\ntwo\nthree\n")
            self.assertIn("new", run("changed", str(f), "--snapshots", snaps))
            self.assertIn("all unchanged", run("changed", str(f), "--snapshots", snaps))
            time.sleep(0.01)
            f.write_text("one\nTWO\nthree\n")
            out = run("changed", str(f), "--snapshots", snaps)
            self.assertIn("changed", out)
            self.assertIn("+TWO", out)
            self.assertIn("-two", out)

    def test_line_count(self):
        with tempfile.TemporaryDirectory() as d:
            f, snaps = Path(d, "a.txt"), str(Path(d, "snaps"))
            f.write_bytes(b"one\ntwo\nthree\n")
            self.assertIn("(3 lines", run("changed", str(f), "--snapshots", snaps))
            self.assertEqual([tw._line_count(b) for b in (b"", b"a", b"a\nb")], [0, 1, 2])

    def test_touched_same_content(self):
        with tempfile.TemporaryDirectory() as d:
            f, snaps = Path(d, "a.txt"), str(Path(d, "snaps"))
            f.write_text("x\n")
            run("changed", str(f), "--snapshots", snaps)
            st = f.stat()
            os.utime(f, ns=(st.st_atime_ns, st.st_mtime_ns + 10_000_000))
            self.assertIn("same content", run("changed", str(f), "--snapshots", snaps))

    def test_dry_run_keeps_snapshot(self):
        with tempfile.TemporaryDirectory() as d:
            f, snaps = Path(d, "a.txt"), str(Path(d, "snaps"))
            f.write_text("x\n")
            run("changed", str(f), "--snapshots", snaps, "--dry-run")
            self.assertIn("new", run("changed", str(f), "--snapshots", snaps))


class Score(unittest.TestCase):
    def transcript(self, d):
        big = "\n".join("line %d" % i for i in range(500))
        p = Path(d, "s.jsonl")
        p.write_text("".join([
            use(1, "Read", {"file_path": "/x/big.py"}), result(1, big),
            use(2, "Read", {"file_path": "/x/big.py"}), result(2, big),
            use(3, "Bash", {"command": "cat /x/log.txt"}), result(3, "a\nb\n"),
            use(4, "Bash", {"command": "make"}), result(4, "boom", True),
            use(5, "Bash", {"command": "make"}), result(5, "boom", True),
            use(6, "Grep", {"pattern": "x"}), result(6, "y" * 30000),
            # the same response written twice must count its usage once
            use(6, "Grep", {"pattern": "x"}),
        ]))
        return p

    def test_kinds(self):
        with tempfile.TemporaryDirectory() as d:
            sinks, usage, n = tw.score(self.transcript(d))
            kinds = {s[0] for s in sinks}
            self.assertEqual(kinds, {"whole-read", "repeat read", "shell-cat", "retry", "big-output"})
            self.assertEqual(usage["turns"], 6)
            big = [s for s in sinks if s[0] == "big-output"][0]
            self.assertEqual(big[1], 7500)

    def test_carried_cost_counts_later_turns(self):
        with tempfile.TemporaryDirectory() as d:
            sinks, _, _ = tw.score(self.transcript(d))
            first = [s for s in sinks if s[0] == "whole-read"][0]
            self.assertEqual(first[5], first[1] * 5)   # read on turn 1 of 6

    def test_second_whole_read_counted_once(self):
        with tempfile.TemporaryDirectory() as d:
            sinks, _, _ = tw.score(self.transcript(d))
            reads = [s for s in sinks if s[0] in ("whole-read", "repeat read")]
            self.assertEqual([(s[0], s[2]) for s in reads], [("whole-read", 1), ("repeat read", 2)])

    def test_edit_between_reads(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d, "s.jsonl")
            p.write_text("".join([use(1, "Read", {"file_path": "/a"}), result(1, "x"),
                                  use(2, "Edit", {"file_path": "/a"}), result(2, "ok"),
                                  use(3, "Read", {"file_path": "/a"}), result(3, "x")]))
            sinks, _, _ = tw.score(p)
            self.assertEqual([s[0] for s in sinks], ["re-read after own edit"])

    def test_poll_from_third_run(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d, "s.jsonl")
            p.write_text("".join(use(i, "Bash", {"command": "git status"}) + result(i, "clean")
                                 for i in range(1, 5)))
            sinks, _, _ = tw.score(p)
            self.assertEqual([(s[0], s[2]) for s in sinks], [("poll", 3), ("poll", 4)])

    def test_json_output(self):
        with tempfile.TemporaryDirectory() as d:
            data = json.loads(run("score", str(self.transcript(d)), "--json"))
            self.assertIn("carried_cache_read_tokens", data)


class Repeats(unittest.TestCase):
    def test_sequence_across_sessions(self):
        with tempfile.TemporaryDirectory() as d:
            files = []
            for k in range(3):
                p = Path(d, "%d.jsonl" % k)
                p.write_text("".join([use(1, "Bash", {"command": "cd /r%d && git pull" % k}), result(1, ""),
                                      use(2, "Bash", {"command": "python build.py %d" % k}), result(2, ""),
                                      use(3, "Bash", {"command": "gh release create v%d" % k}), result(3, "")]))
                files.append(str(p))
            out = run("repeats", *files, "--min-sessions", "3")
            self.assertIn("3 sessions, 3 steps", out)
            self.assertIn("git pull", out)


class Skill(unittest.TestCase):
    def test_findings(self):
        with tempfile.TemporaryDirectory() as d:
            s = Path(d, "demo")
            (s / "references").mkdir(parents=True)
            body = "\n".join("%d. step" % i for i in range(20))
            s.joinpath("SKILL.md").write_text("---\nname: demo\ndescription: %s\n---\n%s\nSee references/index.md\n"
                                              % ("d" * 1100, body))
            s.joinpath("references", "index.md").write_text("read linked.md")
            s.joinpath("references", "linked.md").write_text("z" * 3000)
            s.joinpath("references", "orphan.md").write_text("z" * 3000)
            rep = tw.skill_report(s)
            text = " ".join(m for _, m in rep["findings"])
            self.assertIn("1100 chars", text)
            self.assertIn("script candidate", text)
            self.assertIn("orphan.md", text)
            self.assertNotIn("linked.md (", text)


class Catalog(unittest.TestCase):
    def test_forwards_to_tidy(self):
        self.assertTrue(tw.TIDY.is_file())
        self.assertEqual(tw.main(["catalog", "version"]), 0)


class Hook(unittest.TestCase):
    def test_off_by_default(self):
        os.environ.pop("TOKENWRIGHT_HOOKS", None)
        sys.stdin = io.StringIO(json.dumps({"tool_name": "Read", "tool_input": {"file_path": __file__}}))
        self.assertEqual(run("hook", "pre"), "")

    def test_block_large_read(self):
        with tempfile.TemporaryDirectory() as d:
            f = Path(d, "big.txt")
            f.write_text("x" * 100000)
            os.environ["TOKENWRIGHT_HOOKS"] = "block"
            try:
                sys.stdin = io.StringIO(json.dumps({"tool_name": "Read", "tool_input": {"file_path": str(f)}}))
                out = json.loads(run("hook", "pre"))
                self.assertEqual(out["hookSpecificOutput"]["permissionDecision"], "deny")
                sys.stdin = io.StringIO(json.dumps({"tool_name": "Read",
                                                    "tool_input": {"file_path": str(f), "limit": 20}}))
                self.assertEqual(run("hook", "pre"), "")
            finally:
                os.environ.pop("TOKENWRIGHT_HOOKS", None)


if __name__ == "__main__":
    unittest.main()
