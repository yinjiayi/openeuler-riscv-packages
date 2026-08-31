#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -Eeuo pipefail

repo=yinjiayi/openeuler-riscv-packages
mode=dry-run
while (($#)); do
  case $1 in
    --repo) repo=${2:?}; shift 2 ;;
    --dry-run) mode=dry-run; shift ;;
    --apply) mode=apply; shift ;;
    *) printf 'configure-github: unknown argument %s\n' "$1" >&2; exit 2 ;;
  esac
done
[[ $repo == yinjiayi/openeuler-riscv-packages ]] || {
  printf 'refusing to configure an unexpected repository: %s\n' "$repo" >&2
  exit 2
}
command -v gh >/dev/null || { printf 'gh CLI is required\n' >&2; exit 2; }
command -v jq >/dev/null || { printf 'jq is required\n' >&2; exit 2; }

settings=.github/repository-settings.json
ruleset=.github/rulesets/main.json
labels=.github/labels.json
for file in "$settings" "$ruleset" "$labels"; do
  [[ -s $file ]] || { printf 'missing configuration: %s\n' "$file" >&2; exit 2; }
done

if [[ $mode == dry-run ]]; then
  jq -n --arg repo "$repo" --slurpfile settings "$settings" \
    --slurpfile ruleset "$ruleset" --slurpfile labels "$labels" \
    '{mode:"dry-run",repository:$repo,settings:$settings[0],ruleset:$ruleset[0],labels:$labels[0],writes_performed:false}'
  exit 0
fi

# Authentication comes only from the local gh session or process-level
# GH_TOKEN. Never print, persist, upload, or convert it into an Actions secret.
gh auth status >/dev/null
repository=$(gh api "repos/$repo")
[[ $(jq -r .visibility <<<"$repository") == public ]] || {
  printf 'target repository must already be public\n' >&2
  exit 1
}
[[ $(jq -r .default_branch <<<"$repository") == main ]] || {
  printf 'target default branch must be main\n' >&2
  exit 1
}

gh api --method PATCH "repos/$repo" \
  -F allow_auto_merge=true \
  -F allow_squash_merge=true \
  -F allow_merge_commit=false \
  -F allow_rebase_merge=false \
  -F delete_branch_on_merge=true >/dev/null

default_workflow_permissions=$(jq -r .actions.default_workflow_permissions "$settings")
can_approve_pull_request_reviews=$(jq -r .actions.can_approve_pull_request_reviews "$settings")
[[ $default_workflow_permissions == read ]] || {
  printf 'default Actions token permissions must remain read-only\n' >&2
  exit 1
}
[[ $can_approve_pull_request_reviews == true ]] || {
  printf 'Actions must be permitted to create the reviewed digest-lock PR\n' >&2
  exit 1
}
gh api --method PUT "repos/$repo/actions/permissions/workflow" \
  -f "default_workflow_permissions=$default_workflow_permissions" \
  -F "can_approve_pull_request_reviews=$can_approve_pull_request_reviews" >/dev/null

fork_approval_policy=$(jq -r .actions.fork_pull_request_approval_policy "$settings")
[[ $fork_approval_policy == first_time_contributors_new_to_github ]] || {
  printf 'fork workflow approval policy must allow established contributors to run automatically\n' >&2
  exit 1
}
gh api --method PUT "repos/$repo/actions/permissions/fork-pr-contributor-approval" \
  -f "approval_policy=$fork_approval_policy" >/dev/null

while IFS= read -r label; do
  name=$(jq -r .name <<<"$label")
  color=$(jq -r .color <<<"$label")
  description=$(jq -r .description <<<"$label")
  if gh api "repos/$repo/labels/$name" >/dev/null 2>&1; then
    gh api --method PATCH "repos/$repo/labels/$name" \
      -f "new_name=$name" -f "color=$color" -f "description=$description" >/dev/null
  else
    gh api --method POST "repos/$repo/labels" \
      -f "name=$name" -f "color=$color" -f "description=$description" >/dev/null
  fi
done < <(jq -c '.[]' "$labels")

while IFS=$'\t' read -r name value; do
  if gh api "repos/$repo/actions/variables/$name" >/dev/null 2>&1; then
    gh api --method PATCH "repos/$repo/actions/variables/$name" -f "value=$value" >/dev/null
  else
    gh api --method POST "repos/$repo/actions/variables" -f "name=$name" -f "value=$value" >/dev/null
  fi
done < <(jq -r '.actions_variables | to_entries[] | [.key,.value] | @tsv' "$settings")

if gh api "repos/$repo/pages" >/dev/null 2>&1; then
  gh api --method PUT "repos/$repo/pages" -f build_type=workflow >/dev/null
else
  gh api --method POST "repos/$repo/pages" -f build_type=workflow >/dev/null
fi

ruleset_name=$(jq -r .name "$ruleset")
ruleset_id=$(gh api "repos/$repo/rulesets" --paginate \
  --jq ".[] | select(.name == \"$ruleset_name\") | .id" | head -n 1)
if [[ -n $ruleset_id ]]; then
  gh api --method PUT "repos/$repo/rulesets/$ruleset_id" --input "$ruleset" >/dev/null
else
  gh api --method POST "repos/$repo/rulesets" --input "$ruleset" >/dev/null
fi

applied=$(gh api "repos/$repo/rulesets" --paginate \
  --jq ".[] | select(.name == \"$ruleset_name\") | {id,name,enforcement}")
applied_fork_policy=$(gh api "repos/$repo/actions/permissions/fork-pr-contributor-approval" \
  --jq .approval_policy)
[[ $applied_fork_policy == "$fork_approval_policy" ]] || {
  printf 'fork workflow approval policy readback mismatch\n' >&2
  exit 1
}
jq -n --arg repo "$repo" --argjson ruleset "$applied" \
  --arg fork_approval_policy "$applied_fork_policy" \
  '{mode:"apply",repository:$repo,ruleset:$ruleset,fork_approval_policy:$fork_approval_policy,writes_performed:true,actions_secrets_created:false}'
