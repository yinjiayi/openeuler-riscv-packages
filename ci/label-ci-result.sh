#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -Eeuo pipefail

repo=${GITHUB_REPOSITORY:?}
pr_number=${PR_NUMBER:?}
expected_sha=${EXPECTED_HEAD_SHA:?}
head_repo=${HEAD_REPOSITORY:?}
association=${AUTHOR_ASSOCIATION:-}
artifact_dir=${ARTIFACT_DIR:-artifacts/all-results}
overall=${OVERALL_RESULT:-failure}

trusted=false
case $association in
  OWNER|MEMBER|COLLABORATOR) trusted=true ;;
esac
case ${PR_AUTHOR:-} in
  yinjiayi|github-actions\[bot\]|dependabot\[bot\]) trusted=true ;;
esac

if [[ $head_repo != "$repo" || $trusted != true ]]; then
  printf 'CI state labels are not written for an untrusted or fork PR\n'
  exit 0
fi

current_sha=$(gh api "repos/${repo}/pulls/${pr_number}" --jq .head.sha)
if [[ $current_sha != "$expected_sha" ]]; then
  printf 'PR head moved from %s to %s; refusing to label stale results\n' "$expected_sha" "$current_sha" >&2
  exit 1
fi

ensure_label() {
  local name=$1 color=$2 description=$3
  gh api "repos/${repo}/labels/${name}" >/dev/null 2>&1 || \
    gh api --method POST "repos/${repo}/labels" \
      -f "name=${name}" -f "color=${color}" -f "description=${description}" >/dev/null
}

add_label() {
  gh api --method POST "repos/${repo}/issues/${pr_number}/labels" \
    -f "labels[]=$1" >/dev/null
}

remove_label() {
  gh api --method DELETE "repos/${repo}/issues/${pr_number}/labels/$1" >/dev/null 2>&1 || true
}

ensure_label repair-queued d93f0b 'Trusted CI failure is queued for local Codex repair'
ensure_label codex-repairing fbca04 'A local Codex repair lease is active'
ensure_label needs-native-riscv b60205 'Requires native riscv64 validation; auto-merge is blocked'
ensure_label qemu-limitation e99695 'QEMU user-mode cannot provide the required validation'
ensure_label ci-passed 0e8a16 'All required package checks passed for the current head SHA'

if [[ $overall == success ]]; then
  remove_label repair-queued
  remove_label codex-repairing
  remove_label qemu-limitation
  add_label ci-passed
  exit 0
fi

remove_label ci-passed
if [[ -d $artifact_dir ]] && grep -RIEq '"?(status|classification)"?[[:space:]]*:[[:space:]]*"needs-native-riscv"' "$artifact_dir"; then
  remove_label repair-queued
  remove_label codex-repairing
  add_label needs-native-riscv
elif [[ -d $artifact_dir ]] && grep -RIEq '"?(status|classification)"?[[:space:]]*:[[:space:]]*"qemu-limitation"' "$artifact_dir"; then
  remove_label repair-queued
  remove_label codex-repairing
  add_label qemu-limitation
else
  remove_label codex-repairing
  add_label repair-queued
fi

