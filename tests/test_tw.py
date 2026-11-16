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
            self.assertEqual(big[1], tw.tokens(30000))

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

    def test_debug_loop_on_third_failure_in_a_row(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d, "s.jsonl")
            calls = [use(i, "Bash", {"command": "build %d" % i}) + result(i, "boom", error=True) for i in range(1, 5)]
            calls.append(use(5, "Bash", {"command": "build ok"}) + result(5, "ok"))
            calls += [use(i, "Bash", {"command": "x %d" % i}) + result(i, "boom", error=True) for i in (6, 7)]
            p.write_text("".join(calls))
            sinks, _, _ = tw.score(p)
            self.assertEqual([(s[0], s[2]) for s in sinks], [("debug-loop", 3)])

    def test_repeated_result_record_counted_once(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d, "s.jsonl")
            p.write_text(use(1, "Grep", {"pattern": "x"}) + result(1, "y" * 30000) * 2)
            sinks, _, _ = tw.score(p)
            self.assertEqual([s[0] for s in sinks], ["big-output"])

    def test_subagent_transcripts_are_scored(self):
        with tempfile.TemporaryDirectory() as d:
            main = self.transcript(d)
            sub = Path(d, "s", "subagents")
            sub.mkdir(parents=True)
            Path(sub, "agent-a1.jsonl").write_text(use(1, "Grep", {"pattern": "z"}) + result(1, "y" * 40000))
            data = json.loads(run("score", str(main), "--json"))
            self.assertEqual(data["subagents"]["count"], 1)
            self.assertEqual(data["subagents"]["usage"]["output_tokens"], 5)
            self.assertEqual(data["subagents"]["waste_tokens"], tw.tokens(40000))
            self.assertTrue(any(s["what"].startswith("[subagent a1]") for s in data["sinks"]))
            text = run("score", str(main))
            self.assertIn("subagents 1:", text)
            self.assertEqual(json.loads(run("score", str(main), "--json", "--no-subagents")).get("subagents"), None)

    def test_json_output(self):
        with tempfile.TemporaryDirectory() as d:
            data = json.loads(run("score", str(self.transcript(d)), "--json"))
            self.assertIn("carried_cache_read_tokens", data)

    def test_cache_read_rates_named(self):
        with tempfile.TemporaryDirectory() as d:
            text = run("score", str(self.transcript(d)))
            self.assertIn("0.025x Fable", text)
            self.assertNotIn("a tenth of input", text)


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

    def test_meter_counts_an_image_at_its_token_cost(self):
        with tempfile.TemporaryDirectory() as d:
            os.environ["TOKENWRIGHT_HOOKS"] = "warn"
            os.environ["TOKENWRIGHT_METER_DIR"] = d
            try:
                ev = {"session_id": "s2", "tool_name": "Read", "tool_input": {"file_path": "shot.png"},
                      "tool_response": {"type": "image", "file": {"base64": "A" * 680000}}}
                sys.stdin = io.StringIO(json.dumps(ev))
                self.assertEqual(run("hook", "post"), "")   # base64 is not what the model pays for
                self.assertEqual(run("meter", "s2").strip(), "tw ~1k")
            finally:
                os.environ.pop("TOKENWRIGHT_HOOKS", None)
                os.environ.pop("TOKENWRIGHT_METER_DIR", None)

    def test_meter_skips_subagent_tool_output(self):
        # T-20261116-7: a subagent's tool output never enters the main context
        with tempfile.TemporaryDirectory() as d:
            os.environ["TOKENWRIGHT_HOOKS"] = "warn"
            os.environ["TOKENWRIGHT_METER_DIR"] = d
            try:
                ev = {"session_id": "s3", "agent_id": "a1", "tool_name": "Grep", "tool_response": "x" * 120000}
                sys.stdin = io.StringIO(json.dumps(ev))
                out = run("hook", "post")
                self.assertNotIn("meter", out)
                self.assertEqual(run("meter", "s3").strip(), "tw ~0k")
            finally:
                os.environ.pop("TOKENWRIGHT_HOOKS", None)
                os.environ.pop("TOKENWRIGHT_METER_DIR", None)

    def test_meter_speaks_once_per_step(self):
        with tempfile.TemporaryDirectory() as d:
            os.environ["TOKENWRIGHT_HOOKS"] = "warn"
            os.environ["TOKENWRIGHT_METER_DIR"] = d
            try:
                ev = {"session_id": "s1", "tool_name": "Read", "tool_response": "x" * 60000}
                sys.stdin = io.StringIO(json.dumps(ev))
                self.assertEqual(run("hook", "post"), "")   # ~26k tokens, below the first step
                sys.stdin = io.StringIO(json.dumps(ev))
                out = json.loads(run("hook", "post"))       # ~52k, crosses 43k
                self.assertIn("meter: ~52k", out["hookSpecificOutput"]["additionalContext"])
                self.assertEqual(run("meter", "s1").strip(), "tw ~52k")
            finally:
                os.environ.pop("TOKENWRIGHT_HOOKS", None)
                os.environ.pop("TOKENWRIGHT_METER_DIR", None)


class Note(unittest.TestCase):
    def test_saved_must_be_a_count(self):
        import contextlib
        self.assertEqual(run("note", "--saved", "12k", "--why", "w").strip(), "noted")
        with contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit):
            tw.main(["note", "--saved", "lots"])


class HookProcess(unittest.TestCase):
    def test_off_exits_before_heavy_imports(self):
        import subprocess
        env = dict(os.environ)
        env.pop("TOKENWRIGHT_HOOKS", None)
        env["PYTHONVERBOSE"] = "1"
        r = subprocess.run([sys.executable, str(Path(tw.__file__)), "hook", "post"], input="{}", text=True,
                           capture_output=True, env=env)
        self.assertEqual(r.returncode, 0)
        self.assertNotIn("import 'argparse'", r.stderr)
        self.assertNotIn("import 'json'", r.stderr)


class Compare(unittest.TestCase):
    def test_best_past_session(self):
        with tempfile.TemporaryDirectory() as d:
            clean = "".join(use(i, "Grep", {"pattern": "p%d" % i}) + result(i, "ok") for i in range(12))
            Path(d, "old.jsonl").write_text(clean)
            now = Path(d, "now.jsonl")
            now.write_text(clean + use(99, "Bash", {"command": "cat big.txt"}) + result(99, "y" * 8000))
            os.utime(Path(d, "old.jsonl"), (1, 1))
            out = run("score", str(now), "--compare", "5")
            self.assertIn("best of 1 past sessions here ~0 (old.jsonl)", out)



class Versions(unittest.TestCase):
    def test_tidy_follows_plugin_version(self):
        import re
        root = Path(tw.__file__).resolve().parents[3]
        tidy = (root / "skills" / "tokenwright-catalog" / "scripts" / "tidy.py").read_text(encoding="utf-8")
        self.assertEqual(re.search(r'^VERSION = "([^"]+)"', tidy, re.M).group(1), tw.VERSION)
        manifest = json.loads((root / ".claude-plugin" / "plugin.json").read_text(encoding="utf-8"))
        self.assertEqual(manifest["version"], tw.VERSION)


class CopilotCli(unittest.TestCase):
    def test_copilot_events_are_scored(self):
        big = "x" * 40000
        recs = [{"type": "user.message", "data": {"content": "hi"}},
                {"type": "session.usage_record", "data": {"usage": {"inputTokens": 100, "outputTokens": 10,
                 "cacheReadTokens": 50, "cacheWriteTokens": 5, "reasoningTokens": 2}}},
                {"type": "tool.execution_start", "data": {"toolCallId": "c1", "toolName": "bash",
                 "arguments": {"command": "make test"}}},
                {"type": "tool.execution_complete", "data": {"toolCallId": "c1", "success": True,
                 "result": {"content": big}}}]
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "events.jsonl"
            p.write_text("\n".join(json.dumps(r) for r in recs), encoding="utf-8")
            sinks, usage, n = tw.score(p)
            self.assertEqual(n, 1)
            self.assertEqual(usage["input_tokens"], 100)
            self.assertEqual(usage["output_tokens"], 12)
            self.assertEqual(usage["cache_read_input_tokens"], 50)
            self.assertTrue(any(s[0] == "big-output" and "Bash" in s[3] for s in sinks))


class TokenRate(unittest.TestCase):
    def test_measured_rate(self):
        # T-20261116-10: current models bill about 2.3 characters a token for tool output, not 4
        self.assertEqual(tw.tokens(2300), 1000)
        self.assertEqual(tw.tokens(1), 1)

    def test_meter_step_keeps_its_character_count(self):
        # the meter was tuned at 25k tokens of chars/4, about 100k characters
        self.assertAlmostEqual(tw.METER_STEP_TOKENS * tw.CHARS_PER_TOKEN, 100000, delta=2000)


if __name__ == "__main__":
    unittest.main()
