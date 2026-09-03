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

[[ ${GITHUB_RUN_ID:-} =~ ^[1-9][0-9]*$ && ${GITHUB_RUN_ATTEMPT:-} =~ ^[1-9][0-9]*$ ]] || {
  printf 'dispatch-required-checks: missing workflow run identity\n' >&2
  exit 2
}
[[ ${GITHUB_REF:-} == refs/heads/main ]] || {
  printf 'dispatch-required-checks: caller is not running from protected main\n' >&2
  exit 2
}
case ${GITHUB_WORKFLOW_REF:-} in
  "$repo/.github/workflows/build-ci-image.yml@refs/heads/main"|\
  "$repo/.github/workflows/catalog-discovery.yml@refs/heads/main") ;;
  *) printf 'dispatch-required-checks: caller workflow is not allowlisted\n' >&2; exit 2 ;;
esac
dispatch_nonce="${GITHUB_RUN_ID}-${GITHUB_RUN_ATTEMPT}-${pr_number}"

current_pr() {
  gh api "repos/$repo/pulls/$pr_number"
}

verify_head() {
  local current
  current=$(current_pr)
  [[ $(jq -r .state <<<"$current") == open ]]
  [[ $(jq -r .merged <<<"$current") == false ]]
  [[ $(jq -r .head.repo.full_name <<<"$current") == "$repo" ]]
  [[ $(jq -r .head.ref <<<"$current") == "$ref" ]]
  [[ $(jq -r .head.sha <<<"$current") == "$head_sha" ]]
  [[ $(jq -r .base.sha <<<"$current") == "$base_sha" ]]
  [[ $(jq -r .base.ref <<<"$current") == main ]]
  [[ $(jq -r '.auto_merge == null' <<<"$current") == true ]]
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

expected_name="Package CI PR $pr_number $head_sha $dispatch_nonce"
before_runs=$(gh run list --repo "$repo" --workflow package-ci.yml --branch main \
  --event workflow_dispatch --limit 100 --json databaseId,displayTitle,headSha)
before_ids=$(jq --arg name "$expected_name" --arg base "$base_sha" \
  '[.[] | select(.displayTitle == $name and .headSha == $base) | .databaseId]' <<<"$before_runs")
gh workflow run package-ci.yml --repo "$repo" --ref main \
  -f "commit_sha=$head_sha" -f "pr_number=$pr_number" \
  -f "base_sha=$base_sha" -f "dispatch_nonce=$dispatch_nonce" \
  -f publish_to_repo=false >/dev/null

run_id=
for _ in {1..30}; do
  candidates=$(gh run list --repo "$repo" --workflow package-ci.yml --branch main \
    --event workflow_dispatch --limit 100 --json databaseId,displayTitle,headSha,status,conclusion,url)
  run_id=$(jq -r --arg name "$expected_name" --arg base "$base_sha" --argjson before "$before_ids" \
    '[.[] | select(.displayTitle == $name and .headSha == $base and ((.databaseId as $id | $before | index($id)) == null))][0].databaseId // empty' \
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

run_api=$(gh api "repos/$repo/actions/runs/$run_id")
jq -e --argjson id "$run_id" --arg name "$expected_name" --arg base "$base_sha" \
  '.id == $id and .status == "completed" and .conclusion == "success" and
   .display_title == $name and .event == "workflow_dispatch" and
   .head_branch == "main" and .head_sha == $base and
   .path == ".github/workflows/package-ci.yml"' <<<"$run_api" >/dev/null || {
  printf 'dispatch-required-checks: terminal API run identity or conclusion is invalid\n' >&2
  exit 1
}
run=$(gh run view "$run_id" --repo "$repo" --json status,conclusion,displayTitle,headSha,jobs,url)
jq -e --arg name "$expected_name" --arg base "$base_sha" \
  '.status == "completed" and .conclusion == "success" and
   .displayTitle == $name and .headSha == $base' <<<"$run" >/dev/null || {
  printf 'dispatch-required-checks: terminal workflow view is inconsistent\n' >&2
  exit 1
}
verify_head || { printf 'dispatch-required-checks: PR lease changed after the run\n' >&2; exit 1; }

all_success=true
summary='[]'
for context in "${required[@]}"; do
  match_count=$(jq --arg context "$context" '[.jobs[] | select(.name == $context)] | length' <<<"$run")
  conclusion=$(jq -r --arg context "$context" '[.jobs[] | select(.name == $context)][0].conclusion // "missing"' <<<"$run")
  if [[ $match_count != 1 || $conclusion != success ]]; then
    all_success=false
  fi
  summary=$(jq --arg name "$context" --arg conclusion "$conclusion" '. + [{name:$name,conclusion:$conclusion}]' <<<"$summary")
done
[[ $all_success == true ]] || {
  printf 'dispatch-required-checks: one or more required jobs did not succeed exactly once\n' >&2
  exit 1
}
for context in "${required[@]}"; do
  post_status "$context" success 'Protected-main Package CI job: success' "$run_url"
done

document=$(jq -n --argjson schema_version 1 --arg kind bot-pr-required-checks \
  --arg repo "$repo" --argjson pr_number "$pr_number" --arg ref "$ref" \
  --arg head_sha "$head_sha" --arg base_sha "$base_sha" --argjson run_id "$run_id" \
  --arg run_url "$run_url" --arg nonce "$dispatch_nonce" --argjson checks "$summary" --argjson success "$all_success" \
  '{schema_version:$schema_version,kind:$kind,repository:$repo,pr_number:$pr_number,ref:$ref,head_sha:$head_sha,base_sha:$base_sha,dispatch_nonce:$nonce,run_id:$run_id,run_url:$run_url,checks:$checks,success:$success}')
if [[ -n $output ]]; then
  mkdir -p "$(dirname "$output")"
  temporary="${output}.tmp.$$"
  printf '%s\n' "$document" >"$temporary"
  mv -- "$temporary" "$output"
else
  printf '%s\n' "$document"
fi
finalized=true

[[ $all_success == true ]]
