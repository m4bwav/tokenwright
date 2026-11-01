#!/usr/bin/env bash
# Writes last-session.jsonl: a recorded session whose sink is logs/app.log read whole three times.
set -e
python3 "$(dirname "$0")/make_session.py" ./last-session.jsonl
