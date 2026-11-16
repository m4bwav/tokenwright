#!/usr/bin/env bash
# Writes runs/run-01..run-05 (build.log, tests.log, probes.log; about 8,000 lines a run).
set -e
python3 "$(dirname "$0")/make_fixture.py" runs ./runs
