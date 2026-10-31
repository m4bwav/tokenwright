"""Write server.log for the outcome-log case: 4,000 request lines and three ERROR lines.

Generated at eval time so the repository does not carry a 250 KB log.
"""
import random
import sys
from datetime import datetime, timedelta

ERRORS = {813: "ERROR db pool exhausted (max=20)", 2902: "ERROR db pool exhausted (max=20)",
          3551: "ERROR payment timeout order=4417"}


def main(path="server.log"):
    rng = random.Random(20261030)
    t = datetime(2026, 10, 30)
    with open(path, "w", newline="\n") as f:
        for n in range(1, 4001):
            stamp = t.strftime("%Y-%m-%dT%H:%M:%S")
            if n in ERRORS:
                f.write("%s %s\n" % (stamp, ERRORS[n]))
            else:
                level = "WARN" if rng.random() < 0.1 else "INFO"
                f.write("%s %s request ok path=/api/item/%d ms=%d\n" % (
                    stamp, level, rng.randint(1, 999), rng.randint(40, 300)))
            t += timedelta(seconds=1)


if __name__ == "__main__":
    main(*sys.argv[1:])
