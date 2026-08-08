#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -Eeuo pipefail

output=${1:-artifacts/github-state.json}
repo=${GITHUB_REPOSITORY:?}
tmp=$(mktemp -d)
trap 'rm -rf -- "$tmp"' EXIT
mkdir -p "$(dirname "$output")"

gh api --paginate --slurp "repos/${repo}/pulls?state=all&per_page=100&sort=updated&direction=desc" \
  >"$tmp/pull-pages.json"
gh api --paginate --slurp "repos/${repo}/actions/runs?per_page=100" \
  >"$tmp/run-pages.json"
gh api "repos/${repo}" >"$tmp/repository.json"

jq -n \
  --arg generated_at "$(date -u +%Y-%m-%dT%H:%M:%SZ)" \
  --slurpfile repository "$tmp/repository.json" \
  --slurpfile pull_pages "$tmp/pull-pages.json" \
  --slurpfile run_pages "$tmp/run-pages.json" \
  '{
    schema_version: 1,
    generated_at: $generated_at,
    repository: $repository[0],
    pull_requests: ($pull_pages[0] | add),
    workflow_runs: (($run_pages[0] | map(.workflow_runs) | add) // [])
  }' >"$output"
