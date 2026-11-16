"""Build the fixture for multiturn-long-job.

make_fixture.py runs DIR   writes DIR/run-01..run-05, each with build.log, tests.log and probes.log
                           (about 8,000 lines a run; the scaffold calls this)
make_fixture.py answers    prints the expected report.csv rows
"""
import random
import sys
from pathlib import Path

RUNS = ["run-%02d" % i for i in range(1, 6)]
CODES = ["W%04d" % c for c in (1201, 1310, 2044, 3002, 3117, 4520, 5005)]
ENDPOINTS = ["/api/login", "/api/cart", "/api/search", "/api/orders", "/api/profile", "/api/health"]


def build_log(run):
    rnd = random.Random("build" + run)
    weights = [rnd.randint(1, 30) for _ in CODES]
    weights[rnd.randrange(len(CODES))] += 40  # one clear winner, no ties
    out = []
    for i in range(4000):
        if rnd.random() < 0.3:
            code = rnd.choices(CODES, weights)[0]
            out.append("[%05d] WARN [%s] src/mod%02d/file%03d.c:%d: implicit conversion may lose precision"
                       % (i, code, rnd.randrange(40), rnd.randrange(300), rnd.randrange(1, 900)))
        else:
            out.append("[%05d] INFO compiling src/mod%02d/file%03d.c" % (i, rnd.randrange(40), rnd.randrange(300)))
    return out


def tests_log(run):
    rnd = random.Random("tests" + run)
    out = []
    for i in range(2500):
        name = "test_case_%04d" % i
        if rnd.random() < 0.02 + 0.01 * RUNS.index(run):
            out.append("FAIL %s: AssertionError expected %d got %d" % (name, rnd.randrange(99), rnd.randrange(99)))
            out += ["    at frame_%d (suite.py:%d)" % (k, rnd.randrange(900)) for k in range(4)]
        else:
            out.append("PASS %s (%dms)" % (name, rnd.randrange(1, 400)))
    return out


def probes_log(run):
    rnd = random.Random("probes" + run)
    slow = rnd.choice(ENDPOINTS)
    out = []
    for i in range(1500):
        ep = rnd.choice(ENDPOINTS)
        ms = rnd.randrange(20, 900)
        out.append("probe %s status=200 latency=%dms seq=%d" % (ep, ms, i))
    out.insert(rnd.randrange(len(out)), "probe %s status=200 latency=%dms seq=9999" % (slow, 1500 + rnd.randrange(400)))
    return out


def answer(run):
    counts = {}
    for l in build_log(run):
        if " WARN [" in l:
            c = l.split("[")[2][:5]
            counts[c] = counts.get(c, 0) + 1
    top = max(counts, key=counts.get)
    fails = sum(1 for l in tests_log(run) if l.startswith("FAIL "))
    best = max(probes_log(run), key=lambda l: int(l.split("latency=")[1].split("ms")[0]))
    return "%s,%d,%s,%d,%s" % (run, sum(counts.values()), top, fails, best.split()[1])


def write_runs(root):
    for run in RUNS:
        d = Path(root) / run
        d.mkdir(parents=True, exist_ok=True)
        for name, fn in (("build.log", build_log), ("tests.log", tests_log), ("probes.log", probes_log)):
            (d / name).write_text("\n".join(fn(run)) + "\n", encoding="utf-8", newline="\n")


if __name__ == "__main__":
    if sys.argv[1] == "runs":
        write_runs(sys.argv[2])
    else:
        print("run,warnings,top_warning,failed_tests,slowest_probe")
        for r in RUNS:
            print(answer(r))
