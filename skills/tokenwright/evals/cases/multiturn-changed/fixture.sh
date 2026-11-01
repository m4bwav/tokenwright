#!/usr/bin/env bash
# Seeds the tw.py snapshot from turn 1 (settings v1), then puts the user's edit in place.
set -e
py=python3; "$py" -c "" 2>/dev/null || py=python
here="$(dirname "$0")"
"$py" "$here/make_history.py" settings v1 ./settings.py
"$py" "$here/../../../scripts/tw.py" changed settings.py >/dev/null
"$py" "$here/make_history.py" settings v2 ./settings.py
