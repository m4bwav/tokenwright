"""A/B eval with token counts per arm. Run in WSL (Bash cases need Linux).

  python3 scripts/ab_eval.py "<case glob>" [--runs-dir ~/ab] [--max-cost 3]

Arm "with" is this plugin. Arm "stub" is a copy with no skills and no hooks,
so history cases (which the harness runs single-arm) get a baseline too.
Both run with --ablation none --keep-temp; tokens come from each kept
sandbox's out/trace.jsonl. Prints one line per run and a mean per arm.
Caveat (T-20261116-2): a history file that shows the plugin's commands
teaches them to the stub arm as well.
"""
import argparse, glob, json, os, re, shutil, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def make_stub(dst):
    shutil.rmtree(dst, ignore_errors=True)
    os.makedirs(os.path.join(dst, "noskills"))
    ev = os.path.join(ROOT, "skills", "tokenwright", "evals")
    shutil.copytree(ev, os.path.join(dst, "skills", "tokenwright", "evals"))
    p = json.load(open(os.path.join(ROOT, "plugin.json"), encoding="utf-8"))
    p.update(name=p["name"] + "-stub", skills="./noskills")
    p.pop("hooks", None)
    json.dump(p, open(os.path.join(dst, "plugin.json"), "w"), indent=1)


def tokens(sandbox):
    t = dict(input=0, output=0, cache_read=0, cache_write=0)
    for f in glob.glob(os.path.join(sandbox, "out", "trace.jsonl")):
        for line in open(f, encoding="utf-8", errors="replace"):
            try:
                x = json.loads(line)
            except ValueError:
                continue
            if x.get("type") != "assistant":
                continue
            u = (x.get("message") or {}).get("usage") or {}
            t["input"] += u.get("input_tokens", 0)
            t["output"] += u.get("output_tokens", 0)
            t["cache_read"] += u.get("cache_read_input_tokens", 0)
            t["cache_write"] += u.get("cache_creation_input_tokens", 0)
    return t


def run_arm(arm, plugin, case, out, max_cost):
    js, log = os.path.join(out, arm + ".json"), os.path.join(out, arm + ".log")
    cmd = ["claude", "plugin", "eval", plugin, "--no-publish", "--trust-plugin",
           "--scaffold", "--ablation", "none", "--keep-temp", "--allow-tools",
           "Bash", "Write", "Edit", "--case", case, "--max-cost-usd", str(max_cost),
           "--json", js]
    env = dict(os.environ, TMPDIR=os.environ.get("TMPDIR") or os.path.expanduser("~/evaltmp"))
    os.makedirs(env["TMPDIR"], exist_ok=True)
    with open(log, "w") as fh:
        subprocess.run(cmd, stdout=fh, stderr=subprocess.STDOUT, env=env)
    rows = []
    res = json.load(open(js))
    for c in res["cases"]:
        for r in list(c["arms"].values())[0]:
            sb = os.path.dirname(os.path.dirname(r.get("tracePath") or ""))
            subprocess.run(["chmod", "700", sb], stderr=subprocess.DEVNULL)
            rows.append(dict(arm=arm, case=c["name"], score=r.get("score"),
                             cost=round(r.get("costUsd") or 0, 4), turns=r.get("turns"),
                             **tokens(sb)))
    return rows


def main():
    a = argparse.ArgumentParser()
    a.add_argument("case")
    a.add_argument("--runs-dir", default=os.path.expanduser("~/ab"))
    a.add_argument("--max-cost", type=float, default=3)
    o = a.parse_args()
    os.makedirs(o.runs_dir, exist_ok=True)
    stub = os.path.join(o.runs_dir, "stub-plugin")
    make_stub(stub)
    rows = run_arm("with", ROOT, o.case, o.runs_dir, o.max_cost)
    rows += run_arm("stub", stub, o.case, o.runs_dir, o.max_cost)
    for r in rows:
        print(json.dumps(r))
    for arm in ("with", "stub"):
        rs = [r for r in rows if r["arm"] == arm]
        if rs:
            m = {k: round(sum(r[k] or 0 for r in rs) / len(rs), 3) for k in ("score", "cost", "cache_read", "output")}
            print(arm, "mean", json.dumps(m))
    json.dump(rows, open(os.path.join(o.runs_dir, "ab.json"), "w"), indent=1)


if __name__ == "__main__":
    sys.exit(main())
