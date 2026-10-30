# Script templates

## Python (standard library)

```python
#!/usr/bin/env python3
"""<job>: one line on what it does. Usage: python <job>.py <input> [--dry-run]"""
import argparse, subprocess, sys
from pathlib import Path


def run(cmd, dry):
    if dry:
        print("would run:", " ".join(cmd))
        return ""
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode:
        sys.exit("FAILED %s (exit %d): %s" % (cmd[0], r.returncode, r.stderr.strip().splitlines()[-1:]))
    return r.stdout


def main():
    p = argparse.ArgumentParser()
    p.add_argument("target")
    p.add_argument("--dry-run", action="store_true")
    a = p.parse_args()
    target = Path(a.target)
    if (target / ".done").exists():          # idempotent: skip finished work
        print("SKIP already done:", target)
        return
    out = run(["echo", str(target)], a.dry_run)
    log = target / "job.log"
    if not a.dry_run:
        log.write_text(out)
    print("OK %s: %d lines of output in %s" % (target, out.count("\n"), log))   # short, for the judge


if __name__ == "__main__":
    main()
```

## Shell

```sh
#!/bin/sh
# <job>: one line. Usage: job.sh <target> [--dry-run]
set -eu
target=$1; dry=${2:-}
do_run() { if [ "$dry" = "--dry-run" ]; then echo "would run: $*"; else "$@"; fi; }
log=$(mktemp)
do_run some-command "$target" >"$log" 2>&1 || { echo "FAILED some-command; last lines:"; tail -n 5 "$log"; exit 1; }
echo "OK $target ($(wc -l <"$log") log lines in $log)"
```

## Output rules

- One status line per unit of work: `OK`, `SKIP`, `FAILED`, plus the number that matters.
- Full logs to a file; print the path.
- On failure print the last few lines of the error, not the whole log.
