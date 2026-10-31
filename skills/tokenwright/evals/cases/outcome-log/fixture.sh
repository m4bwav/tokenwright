#!/usr/bin/env bash
# Generate the fixture into the empty eval workspace.
set -e
"$(command -v python3 || command -v python)" "$(dirname "$0")/../../fixtures/make_server_log.py" server.log
