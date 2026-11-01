#!/usr/bin/env bash
# Writes logs/<date>/<service>.log for the three days the history and prompt name.
set -e
python3 "$(dirname "$0")/make_fixture.py" logs ./logs
