import importlib.util, json, os, tempfile, unittest

HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("ab_eval", os.path.join(HERE, "..", "scripts", "ab_eval.py"))
ab = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ab)


def agg(runs):
    return {"startedAt": "2026-11-17T00:00:00Z", "suite": {"ablation": "none"},
            "cases": [{"name": "outcome-x", "arms": {"with": runs}}, {"name": "only-with", "arms": {"with": runs}}]}


class MergeTest(unittest.TestCase):
    def test_stub_becomes_without_arm(self):
        d = tempfile.mkdtemp()
        w, s = os.path.join(d, "with.json"), os.path.join(d, "stub.json")
        json.dump(agg([{"score": 1, "costUsd": 0.1}]), open(w, "w"))
        st = agg([{"score": 0, "costUsd": 0.2}])
        st["cases"] = st["cases"][:1]
        json.dump(st, open(s, "w"))
        n = ab.merge(w, s, os.path.join(d, "merged"))
        out = json.load(open(os.path.join(d, "merged", "aggregate-result.json")))
        self.assertEqual(n, 1)
        self.assertEqual(out["suite"]["ablation"], "with-without")
        arms = out["cases"][0]["arms"]
        self.assertEqual(arms["with"][0]["costUsd"], 0.1)
        self.assertEqual(arms["without"][0]["costUsd"], 0.2)


if __name__ == "__main__":
    unittest.main()


class RunsFlagTest(unittest.TestCase):
    def test_runs_passed_to_plugin_eval(self):
        seen = []
        real = ab.subprocess.run
        ab.subprocess.run = lambda cmd, **k: seen.append(cmd)
        try:
            with tempfile.TemporaryDirectory() as d:
                json.dump({"cases": []}, open(os.path.join(d, "with.json"), "w"))
                ab.run_arm("with", d, "x", d, 1, runs=6)
        finally:
            ab.subprocess.run = real
        self.assertEqual(seen[0][-2:], ["--runs", "6"])
