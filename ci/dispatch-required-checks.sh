#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -Eeuo pipefail

repo=
pr_number=
ref=
head_sha=
base_sha=
output=
while (($#)); do
  case $1 in
    --repo) repo=${2:?}; shift 2 ;;
    --pr-number) pr_number=${2:?}; shift 2 ;;
    --ref) ref=${2:?}; shift 2 ;;
    --head-sha) head_sha=${2:?}; shift 2 ;;
    --base-sha) base_sha=${2:?}; shift 2 ;;
    --output) output=${2:?}; shift 2 ;;
    --help)
      printf '%s\n' 'usage: dispatch-required-checks.sh --repo OWNER/REPO --pr-number N --ref BRANCH --head-sha SHA --base-sha SHA [--output FILE]'
      exit 0
      ;;
    *) printf 'dispatch-required-checks: unknown argument %s\n' "$1" >&2; exit 2 ;;
  esac
done

[[ $repo == yinjiayi/openeuler-riscv-packages ]] || {
  printf 'dispatch-required-checks: refusing unexpected repository %s\n' "$repo" >&2
  exit 2
}
[[ $pr_number =~ ^[1-9][0-9]*$ ]] || { printf 'dispatch-required-checks: invalid PR number\n' >&2; exit 2; }
[[ $ref =~ ^[A-Za-z0-9._/-]+$ && $ref != */../* && $ref != ../* && $ref != */.. ]] || {
  printf 'dispatch-required-checks: invalid branch ref\n' >&2
  exit 2
}
[[ $head_sha =~ ^[0-9a-f]{40}$ && $base_sha =~ ^[0-9a-f]{40}$ ]] || {
  printf 'dispatch-required-checks: head and base must be exact commit SHAs\n' >&2
  exit 2
}
command -v gh >/dev/null || { printf 'dispatch-required-checks: gh is required\n' >&2; exit 2; }
command -v jq >/dev/null || { printf 'dispatch-required-checks: jq is required\n' >&2; exit 2; }

required=(metadata-validate source-verify rpmbuild-riscv64 rpm-install-smoke patch-policy merge-policy)
workflow_url="https://github.com/$repo/actions/workflows/package-ci.yml"
run_url=$workflow_url
finalized=false

current_pr() {
  gh api "repos/$repo/pulls/$pr_number"
}

verify_head() {
  local current
  current=$(current_pr)
  [[ $(jq -r .state <<<"$current") == open ]]
  [[ $(jq -r .head.repo.full_name <<<"$current") == "$repo" ]]
  [[ $(jq -r .head.ref <<<"$current") == "$ref" ]]
  [[ $(jq -r .head.sha <<<"$current") == "$head_sha" ]]
  [[ $(jq -r .base.sha <<<"$current") == "$base_sha" ]]
}

post_status() {
  local context=$1 state=$2 description=$3 target=$4
  gh api --method POST "repos/$repo/statuses/$head_sha" \
    -f "state=$state" -f "context=$context" -f "description=$description" \
    -f "target_url=$target" >/dev/null
}

mark_error_on_exit() {
  local status=$?
  if ((status != 0)) && [[ $finalized != true ]] && verify_head >/dev/null 2>&1; then
    for context in "${required[@]}"; do
      post_status "$context" error 'Bot PR check orchestration failed closed' "$run_url" || true
    done
  fi
  return "$status"
}
trap mark_error_on_exit EXIT

verify_head
for context in "${required[@]}"; do
  post_status "$context" pending 'Waiting for exact-head Package CI job' "$workflow_url"
done

before_runs=$(gh run list --repo "$repo" --workflow package-ci.yml --branch "$ref" \
  --event workflow_dispatch --limit 30 --json databaseId,headSha)
before_ids=$(jq --arg head "$head_sha" '[.[] | select(.headSha == $head) | .databaseId]' <<<"$before_runs")
gh workflow run package-ci.yml --repo "$repo" --ref "$ref" -f "base_sha=$base_sha" >/dev/null

run_id=
for _ in {1..30}; do
  candidates=$(gh run list --repo "$repo" --workflow package-ci.yml --branch "$ref" \
    --event workflow_dispatch --limit 30 --json databaseId,headSha,status,conclusion,url)
  run_id=$(jq -r --arg head "$head_sha" --argjson before "$before_ids" \
    '[.[] | select(.headSha == $head and ((.databaseId as $id | $before | index($id)) == null))][0].databaseId // empty' \
    <<<"$candidates")
  [[ -n $run_id ]] && break
  sleep 2
done
[[ -n $run_id ]] || { printf 'dispatch-required-checks: dispatched run was not observable\n' >&2; exit 1; }

run_url="https://github.com/$repo/actions/runs/$run_id"
set +e
gh run watch "$run_id" --repo "$repo" --exit-status --interval 5
watch_status=$?
set -e

run=$(gh run view "$run_id" --repo "$repo" --json status,conclusion,headSha,jobs,url)
[[ $(jq -r .status <<<"$run") == completed ]]
[[ $(jq -r .headSha <<<"$run") == "$head_sha" ]]
verify_head

all_success=true
summary='[]'
for context in "${required[@]}"; do
  match_count=$(jq --arg context "$context" '[.jobs[] | select(.name == $context)] | length' <<<"$run")
  conclusion=$(jq -r --arg context "$context" '[.jobs[] | select(.name == $context)][0].conclusion // "missing"' <<<"$run")
  if [[ $match_count == 1 && $conclusion == success ]]; then
    state=success
  else
    state=failure
    all_success=false
  fi
  post_status "$context" "$state" "Package CI job: $conclusion" "$run_url"
  summary=$(jq --arg name "$context" --arg conclusion "$conclusion" '. + [{name:$name,conclusion:$conclusion}]' <<<"$summary")
done
finalized=true

document=$(jq -n --argjson schema_version 1 --arg kind bot-pr-required-checks \
  --arg repo "$repo" --argjson pr_number "$pr_number" --arg ref "$ref" \
  --arg head_sha "$head_sha" --arg base_sha "$base_sha" --argjson run_id "$run_id" \
  --arg run_url "$run_url" --argjson checks "$summary" --argjson success "$all_success" \
  '{schema_version:$schema_version,kind:$kind,repository:$repo,pr_number:$pr_number,ref:$ref,head_sha:$head_sha,base_sha:$base_sha,run_id:$run_id,run_url:$run_url,checks:$checks,success:$success}')
if [[ -n $output ]]; then
  mkdir -p "$(dirname "$output")"
  temporary="${output}.tmp.$$"
  printf '%s\n' "$document" >"$temporary"
  mv -- "$temporary" "$output"
else
  printf '%s\n' "$document"
fi

[[ $watch_status == 0 && $all_success == true ]]
