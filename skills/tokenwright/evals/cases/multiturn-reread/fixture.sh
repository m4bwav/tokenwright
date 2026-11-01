#!/usr/bin/env bash
# The file as it is after the user's edit between turns (REQUEST_TIMEOUT 30 -> 45).
set -e
py=python3; "$py" -c "" 2>/dev/null || py=python
"$py" "$(dirname "$0")/make_history.py" settings v2 ./settings.py
