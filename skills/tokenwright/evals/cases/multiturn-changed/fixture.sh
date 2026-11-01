#!/usr/bin/env bash
# Seeds the tw.py snapshot from turn 1 (settings_v1.py), then puts the user's edit in place.
set -e
here="$(dirname "$0")"
cp "$here/settings_v1.py" ./settings.py
python3 "$here/../../../scripts/tw.py" changed settings.py >/dev/null
cp "$here/settings_v2.py" ./settings.py
