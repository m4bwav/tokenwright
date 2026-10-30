#!/usr/bin/env bash
# Copy the fixture into the empty eval workspace.
set -e
cp -r "$(dirname "$0")/../../fixtures/inventory.py" .
