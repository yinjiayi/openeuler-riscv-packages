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

# Requiring a context that is absent from an existing exact PR head would
# strand that PR. Prove complete, trusted legacy coverage before any write.
audit_output=${REQUIRED_CONTEXT_AUDIT_OUTPUT:-work/github-required-context-audit.json}
[[ -x ci/audit-required-context.py ]] || {
  printf 'required-context audit gate is missing or not executable\n' >&2
  exit 1
}
mkdir -p -- "$(dirname -- "$audit_output")"
run_required_context_audit() {
  if ! ci/audit-required-context.py \
       --repository "$repo" \
       --context configure \
       --expected-workflow "Auto Merge Policy" \
       --expected-app github-actions \
       --output "$audit_output" >/dev/null; then
    printf 'required-context audit failed; inspect %s\n' "$audit_output" >&2
    return 1
  fi
}
run_required_context_audit

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

ruleset_projection='
  {
    name: .name,
    target: .target,
    enforcement: .enforcement,
    bypass_actors: .bypass_actors,
    conditions: {
      ref_name: {
        include: .conditions.ref_name.include,
        exclude: .conditions.ref_name.exclude
      }
    },
    rules: [
      .rules[] |
      if .type == "pull_request" then
        {
          type: .type,
          parameters: {
            allowed_merge_methods: .parameters.allowed_merge_methods,
            dismiss_stale_reviews_on_push: .parameters.dismiss_stale_reviews_on_push,
            require_code_owner_review: .parameters.require_code_owner_review,
            require_last_push_approval: .parameters.require_last_push_approval,
            required_approving_review_count: .parameters.required_approving_review_count,
            required_review_thread_resolution: .parameters.required_review_thread_resolution
          }
        }
      elif .type == "required_status_checks" then
        {
          type: .type,
          parameters: {
            strict_required_status_checks_policy: .parameters.strict_required_status_checks_policy,
            do_not_enforce_on_create: .parameters.do_not_enforce_on_create,
            required_status_checks: [
              .parameters.required_status_checks[] |
              {context: .context, integration_id: .integration_id}
            ]
          }
        }
      else
        {type: .type}
      end
    ]
  }
'
ruleset_write_projection='
  {
    name: .name,
    target: .target,
    enforcement: .enforcement,
    bypass_actors: .bypass_actors,
    conditions: .conditions,
    rules: .rules
  }
'
ruleset_name=$(jq -r .name "$ruleset")
desired_policy=$(jq -cS "$ruleset_projection" "$ruleset")
jq -e '
  has("bypass_actors") and (.bypass_actors | type == "array") and .bypass_actors == [] and
  (.conditions | type == "object") and
  (.conditions.ref_name | type == "object") and
  (.conditions.ref_name.include | type == "array") and
  (.conditions.ref_name.exclude | type == "array") and
  (.rules | type == "array")
' \
  "$ruleset" >/dev/null || {
  printf 'configured ruleset must explicitly contain an empty bypass actor list\n' >&2
  exit 1
}

# Close the long provisioning interval with a second stable snapshot directly
# before the protection mutation.
run_required_context_audit
rulesets_before=$(gh api "repos/$repo/rulesets" --paginate --slurp)
[[ $(jq -r 'type == "array" and all(.[]; type == "array")' <<<"$rulesets_before") == true ]] || {
  printf 'ruleset listing did not return paginated arrays\n' >&2
  exit 1
}
ruleset_matches=$(jq -c --arg name "$ruleset_name" '[.[][] | select(.name == $name)]' \
  <<<"$rulesets_before")
ruleset_match_count=$(jq -r length <<<"$ruleset_matches")
(( ruleset_match_count <= 1 )) || {
  printf 'configured ruleset name is not unique\n' >&2
  exit 1
}
ruleset_id=$(jq -r '.[0].id // empty' <<<"$ruleset_matches")
preexisting_ruleset_ids=$(jq -c '[.[][] | .id | select(type == "number")]' <<<"$rulesets_before")
ruleset_created=false
previous_ruleset_input=
previous_ruleset_policy=

rollback_ruleset() {
  if [[ $ruleset_created == true ]]; then
    gh api --method DELETE "repos/$repo/rulesets/$ruleset_id" >/dev/null || return 1
    remaining=$(gh api "repos/$repo/rulesets" --paginate --slurp) || return 1
    jq -e --argjson id "$ruleset_id" \
      'type == "array" and all(.[]; type == "array") and all(.[][]; .id != $id)' \
      <<<"$remaining" >/dev/null
    return
  fi

  gh api --method PUT "repos/$repo/rulesets/$ruleset_id" --input - \
    <<<"$previous_ruleset_input" >/dev/null || return 1
  restored=$(gh api "repos/$repo/rulesets/$ruleset_id") || return 1
  jq -e --argjson id "$ruleset_id" --arg name "$ruleset_name" --arg repo "$repo" \
    '.id == $id and .name == $name and .source == $repo and .source_type == "Repository"' \
    <<<"$restored" >/dev/null || return 1
  restored_policy=$(jq -cS "$ruleset_projection" <<<"$restored") || return 1
  [[ $restored_policy == "$previous_ruleset_policy" ]]
}

discover_created_ruleset() {
  current=$(gh api "repos/$repo/rulesets" --paginate --slurp) || return 1
  candidates=$(jq -c --arg name "$ruleset_name" --argjson before "$preexisting_ruleset_ids" '
    [.[][] |
      select(.name == $name and (.id | type) == "number") |
      select((.id as $id | $before | index($id)) == null)
    ]' <<<"$current") || return 1
  [[ $(jq -r length <<<"$candidates") == 1 ]] || return 1
  ruleset_id=$(jq -r '.[0].id' <<<"$candidates")
  [[ $ruleset_id =~ ^[0-9]+$ ]] || return 1
  ruleset_created=true
}

if [[ -n $ruleset_id ]]; then
  previous_ruleset=$(gh api "repos/$repo/rulesets/$ruleset_id")
  jq -e --argjson id "$ruleset_id" --arg name "$ruleset_name" --arg repo "$repo" '
    .id == $id and .name == $name and .source == $repo and .source_type == "Repository" and
    has("bypass_actors") and (.bypass_actors | type == "array") and
    (.conditions | type == "object") and
    (.conditions.ref_name | type == "object") and
    (.conditions.ref_name.include | type == "array") and
    (.conditions.ref_name.exclude | type == "array") and
    (.rules | type == "array")
  ' \
    <<<"$previous_ruleset" >/dev/null || {
    printf 'existing ruleset readback identity or policy shape is invalid\n' >&2
    exit 1
  }
  previous_ruleset_input=$(jq -cS "$ruleset_write_projection" <<<"$previous_ruleset")
  previous_ruleset_policy=$(jq -cS "$ruleset_projection" <<<"$previous_ruleset")
  if ! gh api --method PUT "repos/$repo/rulesets/$ruleset_id" --input "$ruleset" >/dev/null; then
    printf 'ruleset update failed with an unknown live result; attempting exact policy rollback\n' >&2
    rollback_ruleset || printf 'ruleset rollback could not be verified; inspect the live policy immediately\n' >&2
    exit 1
  fi
else
  if ! created=$(gh api --method POST "repos/$repo/rulesets" --input "$ruleset"); then
    printf 'ruleset creation failed with an unknown live result; attempting discovered-rule rollback\n' >&2
    if discover_created_ruleset; then
      rollback_ruleset || printf 'ruleset rollback could not be verified; inspect the live policy immediately\n' >&2
    else
      printf 'created ruleset identity could not be proven; inspect the live policy immediately\n' >&2
    fi
    exit 1
  fi
  if ! ruleset_id=$(jq -er 'if type == "object" and (.id | type) == "number" then .id else error("missing numeric id") end' \
      <<<"$created") || [[ ! $ruleset_id =~ ^[0-9]+$ ]]; then
    printf 'created ruleset did not return a numeric id; attempting discovered-rule rollback\n' >&2
    if discover_created_ruleset; then
      rollback_ruleset || printf 'ruleset rollback could not be verified; inspect the live policy immediately\n' >&2
    else
      printf 'created ruleset identity could not be proven; inspect the live policy immediately\n' >&2
    fi
    exit 1
  fi
  ruleset_created=true
fi

if ! applied_full=$(gh api "repos/$repo/rulesets/$ruleset_id"); then
  printf 'ruleset readback failed after mutation; attempting exact policy rollback\n' >&2
  rollback_ruleset || printf 'ruleset rollback could not be verified; inspect the live policy immediately\n' >&2
  exit 1
fi
if ! jq -e --argjson id "$ruleset_id" --arg name "$ruleset_name" --arg repo "$repo" \
    '.id == $id and .name == $name and
     .source == $repo and .source_type == "Repository" and
     has("bypass_actors") and (.bypass_actors | type == "array") and
     (.conditions | type == "object") and
     (.conditions.ref_name | type == "object") and
     (.conditions.ref_name.include | type == "array") and
     (.conditions.ref_name.exclude | type == "array") and
     (.rules | type == "array")' \
    <<<"$applied_full" >/dev/null; then
  printf 'ruleset readback identity is invalid; attempting exact policy rollback\n' >&2
  rollback_ruleset || printf 'ruleset rollback could not be verified; inspect the live policy immediately\n' >&2
  exit 1
fi
if ! applied_policy=$(jq -ceS "$ruleset_projection" <<<"$applied_full"); then
  printf 'ruleset readback has an invalid policy shape; attempting exact policy rollback\n' >&2
  rollback_ruleset || printf 'ruleset rollback could not be verified; inspect the live policy immediately\n' >&2
  exit 1
fi
[[ $applied_policy == "$desired_policy" ]] || {
  printf 'ruleset readback does not exactly match the configured protection policy\n' >&2
  diff -u <(jq -S "$ruleset_projection" "$ruleset") \
    <(jq -S "$ruleset_projection" <<<"$applied_full") >&2 || true
  rollback_ruleset || printf 'ruleset rollback could not be verified; inspect the live policy immediately\n' >&2
  exit 1
}
applied=$(jq -ce '{id,name,enforcement}' <<<"$applied_full")
applied_fork_policy=$(gh api "repos/$repo/actions/permissions/fork-pr-contributor-approval" \
  --jq .approval_policy)
[[ $applied_fork_policy == "$fork_approval_policy" ]] || {
  printf 'fork workflow approval policy readback mismatch\n' >&2
  exit 1
}
jq -n --arg repo "$repo" --argjson ruleset "$applied" \
  --arg fork_approval_policy "$applied_fork_policy" \
  '{mode:"apply",repository:$repo,ruleset:$ruleset,fork_approval_policy:$fork_approval_policy,writes_performed:true,actions_secrets_created:false}'
