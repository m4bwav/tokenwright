#!/usr/bin/env bash
# Copy the fixture into the eval workspace at the path the prompt names.
set -e
mkdir -p evals/fixtures
cp -r "$(dirname "$0")/../../fixtures/bloated-skill" evals/fixtures/
