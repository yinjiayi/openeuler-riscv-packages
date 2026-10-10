#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -Eeuo pipefail

output=${1:-artifacts/github-state.json}
repo=${GITHUB_REPOSITORY:-${GH_REPOSITORY:?}}
raw=${2:-work/dashboard-private/current-pr-raw}
python3 ci/collect-github-state.py --repository "$repo" --repo-root . \
  --raw-dir "$raw" --output "$output"
