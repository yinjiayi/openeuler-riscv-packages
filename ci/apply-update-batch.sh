#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -Eeuo pipefail

aggregate=
batch_index=
batch_size=20
packages_dir=packages
artifact_dir=${RUNNER_TEMP:-/tmp}/openeuler-update-apply
while (($#)); do
  case $1 in
    --aggregate) aggregate=${2:?}; shift 2 ;;
    --batch-index) batch_index=${2:?}; shift 2 ;;
    --batch-size) batch_size=${2:?}; shift 2 ;;
    --packages-dir) packages_dir=${2:?}; shift 2 ;;
    --artifact-dir) artifact_dir=${2:?}; shift 2 ;;
    *) printf 'apply-update-batch: unknown argument %s\n' "$1" >&2; exit 2 ;;
  esac
done
[[ -f $aggregate && $batch_index =~ ^[0-9]+$ && $batch_size =~ ^[1-9][0-9]*$ ]] || exit 2
mkdir -p "$artifact_dir"

repo=${GITHUB_REPOSITORY:?}
default_branch=$(gh api "repos/${repo}" --jq .default_branch)
git fetch --no-tags origin "$default_branch"
git config user.name github-actions\[bot\]
git config user.email 41898282+github-actions\[bot\]@users.noreply.github.com

start=$((batch_index * batch_size))
end=$((start + batch_size))
mapfile -t updates < <(jq -c --argjson start "$start" --argjson end "$end" \
  '.updates[$start:$end][]' "$aggregate")

ensure_label() {
  local name=$1 color=$2 description=$3
  gh api "repos/${repo}/labels/${name}" >/dev/null 2>&1 || \
    gh api --method POST "repos/${repo}/labels" \
      -f "name=${name}" -f "color=${color}" -f "description=${description}" >/dev/null
}
ensure_label update 1d76db 'Automated stable upstream release update'
ensure_label operation:update 1d76db 'Automated per-package stable update operation'
ensure_label ci-queued 5319e7 'Waiting for required package checks'

for update in "${updates[@]}"; do
  package_id=$(jq -r .package_id <<<"$update")
  target_version=$(jq -r '.version // .latest_version // empty' <<<"$update")
  idempotency_key=$(jq -r .idempotency_key <<<"$update")
  [[ $package_id =~ ^[a-z0-9]+(-[a-z0-9]+)*$ ]] || { printf 'unsafe package id\n' >&2; exit 2; }
  [[ $target_version != *$'\n'* && -n $target_version ]] || { printf 'unsafe target version\n' >&2; exit 2; }
  [[ $idempotency_key == "update:${package_id}:${target_version}" ]] || {
    printf 'unexpected idempotency key for %s\n' "$package_id" >&2
    exit 2
  }

  existing=$(gh pr list --repo "$repo" --state all \
    --search "${idempotency_key} in:body" --json number,state,url --limit 1)
  if [[ $(jq length <<<"$existing") -gt 0 ]]; then
    printf '%s already has an update record: %s\n' "$package_id" "$(jq -r '.[0].url' <<<"$existing")"
    continue
  fi

  safe_version=$(sed -E 's/[^A-Za-z0-9._-]+/-/g; s/^-+//; s/-+$//' <<<"$target_version")
  [[ -n $safe_version ]] || exit 2
  branch="update/${package_id}/${safe_version}"
  git switch --detach "origin/${default_branch}"
  if git ls-remote --exit-code --heads origin "refs/heads/${branch}" >/dev/null 2>&1; then
    git fetch --no-tags origin "refs/heads/${branch}:refs/remotes/origin/${branch}"
    git switch -C "$branch" "origin/${branch}"
    git merge --no-edit "origin/${default_branch}"
  else
    git switch -C "$branch" "origin/${default_branch}"
  fi

  apply_result="${artifact_dir}/apply-${package_id}.json"
  scripts/check-update apply --result "$aggregate" --package "$package_id" \
    --packages-dir "$packages_dir" --output "$apply_result"

  mapfile -t modified < <(git status --porcelain --untracked-files=all | sed -E 's/^.. //')
  ((${#modified[@]} > 0)) || { printf '%s produced no changes\n' "$package_id"; continue; }
  for path in "${modified[@]}"; do
    [[ $path == "${packages_dir}/${package_id}/"* ]] || {
      printf 'update attempted to modify an out-of-scope path: %s\n' "$path" >&2
      exit 2
    }
  done

  git add -- "${packages_dir}/${package_id}"
  git commit -m "Update ${package_id} to ${target_version}"
  git push origin "HEAD:refs/heads/${branch}"

  title=$(jq -r '.suggested_pr.title // empty' "$apply_result")
  [[ -n $title ]] || title="Update ${package_id} to ${target_version}"
  body_file="${artifact_dir}/pr-${package_id}.md"
  jq -r '.suggested_pr.body // empty' "$apply_result" >"$body_file"
  {
    printf '\n<!-- %s -->\n' "$idempotency_key"
    printf '\nAutomated daily stable-release check. All external metadata is treated as untrusted input; required CI remains authoritative.\n'
  } >>"$body_file"
  pr_url=$(gh pr create --repo "$repo" --base "$default_branch" --head "$branch" \
    --title "$title" --body-file "$body_file")
  ensure_label "package:${package_id}" 0e8a16 "Changes only package ${package_id}"
  gh pr edit "$pr_url" --repo "$repo" --add-label update --add-label operation:update \
    --add-label "package:${package_id}" --add-label ci-queued
  printf 'Created %s for %s. Auto-merge is disabled; an explicit maintainer squash merge is required.\n' \
    "$pr_url" "$package_id"
done
