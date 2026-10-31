#!/usr/bin/env bash
# The file as it is after the user's edit between turns (REQUEST_TIMEOUT 30 -> 45).
set -e
cp "$(dirname "$0")/settings_v2.py" ./settings.py
