#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -Eeuo pipefail

baseline_root=/usr/share/openeuler-riscv-ci
bootstrap_path_file=$baseline_root/bootstrap-rpmdb.path
manifest_helper=/usr/local/libexec/openeuler-riscv-ci/rpm-manifest.sh

fail() {
  printf 'target rpmdb finalization failed: %s\n' "$*" >&2
  exit 1
}

validate_db_path() {
  local label=$1
  local value=$2
  local component
  local -a components
  [[ $value =~ ^/[A-Za-z0-9._/-]+$ && $value != / && $value != *//* ]] \
    || fail "$label is not a canonical absolute path"
  IFS=/ read -r -a components <<<"$value"
  for component in "${components[@]}"; do
    [[ $component != . && $component != .. ]] \
      || fail "$label contains a traversal component"
  done
}

[[ -s $bootstrap_path_file && ! -L $bootstrap_path_file ]] \
  || fail 'the recorded bootstrap rpmdb path is missing or unsafe'
[[ -x $manifest_helper && ! -L $manifest_helper ]] \
  || fail 'the shared RPM manifest helper is missing or unsafe'

bootstrap_db=$(<"$bootstrap_path_file")
runtime_db=$(rpm --eval '%{_dbpath}')
validate_db_path 'bootstrap rpmdb path' "$bootstrap_db"
validate_db_path 'target runtime rpmdb path' "$runtime_db"
if [[ $bootstrap_db != "$runtime_db" ]]; then
  [[ $bootstrap_db != "$runtime_db/"* && $runtime_db != "$bootstrap_db/"* ]] \
    || fail 'bootstrap and target runtime rpmdb paths overlap'
fi

[[ -d $bootstrap_db && ! -L $bootstrap_db ]] \
  || fail 'the recorded bootstrap rpmdb directory is missing or unsafe'
[[ -n $(find "$bootstrap_db" -mindepth 1 -maxdepth 1 -print -quit) ]] \
  || fail 'the recorded bootstrap rpmdb directory is empty'
[[ ! -L $runtime_db ]] || fail 'the target runtime rpmdb path is a symlink'

if [[ $bootstrap_db != "$runtime_db" ]]; then
  if [[ ! -d $runtime_db || -z $(find "$runtime_db" -mindepth 1 -maxdepth 1 -print -quit) ]]; then
    install -d -m 0755 "$runtime_db"
    cp -a -- "$bootstrap_db/." "$runtime_db/"
  fi
fi

live_before=$(mktemp)
trap 'rm -f -- "$live_before"' EXIT
"$manifest_helper" >"$live_before"
[[ -s $live_before ]] \
  || fail 'the target runtime cannot read the bootstrap RPM database at its evaluated path'
printf 'target rpmdb finalization: evaluated target RPM database is readable\n'
