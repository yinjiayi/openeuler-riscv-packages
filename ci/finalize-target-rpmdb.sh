#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -Eeuo pipefail

baseline_root=/usr/share/openeuler-riscv-ci
bootstrap_path_file=$baseline_root/bootstrap-rpmdb.path
manifest_helper=/usr/local/libexec/openeuler-riscv-ci/rpm-manifest.sh
bootstrap_version_file=$baseline_root/bootstrap-rpm-version.txt
diagnostic_root=$(mktemp -d)
trap 'rm -rf -- "$diagnostic_root"' EXIT

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

diagnostic() {
  printf 'rpmdb-diagnostic %s\n' "$*" >&2
}

diagnose_db_directory() {
  local label=$1
  local path=$2
  local entry
  local kind
  if [[ ! -d $path || -L $path ]]; then
    diagnostic "directory=$label state=missing-or-unsafe path=$path"
    return
  fi
  diagnostic "directory=$label state=present path=$path"
  while IFS= read -r -d '' entry; do
    kind=$(file --brief -- "$entry" 2>&1) || kind="file-command-failed:$?"
    printf 'rpmdb-diagnostic directory=%s entry=%q stat=' "$label" "${entry##*/}" >&2
    stat -c 'type=%F size=%s mode=%a' -- "$entry" >&2 \
      || diagnostic "directory=$label entry-stat-failed"
    printf 'rpmdb-diagnostic directory=%s entry=%q file-type=%q\n' \
      "$label" "${entry##*/}" "$kind" >&2
  done < <(find "$path" -mindepth 1 -maxdepth 1 -print0 | LC_ALL=C sort -z)
}

probe_query() {
  local label=$1
  shift
  local output=$diagnostic_root/${label}.out
  local errors=$diagnostic_root/${label}.err
  local status
  local count
  local digest
  set +e
  "$@" >"$output" 2>"$errors"
  status=$?
  set -e
  count=$(wc -l <"$output" | tr -d ' ')
  digest=$(sha256sum "$output" | awk '{print $1}')
  diagnostic "probe=$label status=$status record-count=$count output-sha256=$digest"
  if [[ -s $errors ]]; then
    while IFS= read -r line; do
      printf 'rpmdb-diagnostic probe=%s stderr=%q\n' "$label" "$line" >&2
    done < <(head -n 20 "$errors")
  fi
}

probe_db_copy() {
  local label=$1
  local path=$2
  local copy=$diagnostic_root/${label}.db
  if [[ ! -d $path || -L $path ]]; then
    diagnostic "probe=$label state=skipped-missing-or-unsafe"
    return
  fi
  mkdir -m 0700 "$copy"
  if ! cp -a -- "$path/." "$copy/"; then
    diagnostic "probe=$label state=copy-failed"
    return
  fi
  probe_query "$label-copy" rpm --dbpath "$copy" -qa --qf '%{NAME}\n'
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

diagnostic "bootstrap-dbpath=$bootstrap_db"
diagnostic "target-dbpath=$runtime_db"
if [[ -s $bootstrap_version_file && ! -L $bootstrap_version_file ]]; then
  diagnostic "bootstrap-rpm-version=$(<"$bootstrap_version_file")"
else
  diagnostic 'bootstrap-rpm-version=missing'
fi
diagnostic "target-rpm-version=$(rpm --version)"
diagnose_db_directory bootstrap "$bootstrap_db"
if [[ $bootstrap_db == "$runtime_db" ]]; then
  diagnostic 'path-relation=equal'
else
  diagnose_db_directory target-before "$runtime_db"
  diagnostic 'path-relation=different'
fi
probe_db_copy bootstrap "$bootstrap_db"
if [[ $bootstrap_db != "$runtime_db" ]]; then
  probe_db_copy target-before "$runtime_db"
fi
probe_query target-default-before "$manifest_helper"

if [[ $bootstrap_db != "$runtime_db" ]]; then
  if [[ ! -d $runtime_db || -z $(find "$runtime_db" -mindepth 1 -maxdepth 1 -print -quit) ]]; then
    install -d -m 0755 "$runtime_db"
    cp -a -- "$bootstrap_db/." "$runtime_db/"
  fi
fi

live_before=$(mktemp)
trap 'rm -rf -- "$diagnostic_root"; rm -f -- "$live_before"' EXIT
"$manifest_helper" >"$live_before"
probe_query target-default-after "$manifest_helper"
[[ -s $live_before ]] \
  || fail 'the target runtime cannot read the bootstrap RPM database at its evaluated path'
printf 'target rpmdb finalization: evaluated target RPM database is readable\n'
