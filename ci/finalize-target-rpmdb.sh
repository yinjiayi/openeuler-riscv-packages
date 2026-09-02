#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -Eeuo pipefail

baseline_root=/usr/share/openeuler-riscv-ci
bootstrap_path_file=$baseline_root/bootstrap-rpmdb.path
manifest_helper=/usr/local/libexec/openeuler-riscv-ci/rpm-manifest.sh
transport=$baseline_root/rpmdb-header-list.bin
transport_sha=$baseline_root/rpmdb-header-list.sha256
staging_db=$baseline_root/target-rpmdb.staging

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
[[ -s $transport && ! -L $transport && -s $transport_sha && ! -L $transport_sha ]] \
  || fail 'the portable RPM database transport is missing or unsafe'
sha256sum --check \
  <(printf '%s  %s\n' "$(<"$transport_sha")" "$transport")

bootstrap_db=$(<"$bootstrap_path_file")
runtime_db=$(rpm --eval '%{_dbpath}')
validate_db_path 'bootstrap rpmdb path' "$bootstrap_db"
validate_db_path 'target runtime rpmdb path' "$runtime_db"
validate_db_path 'target staging rpmdb path' "$staging_db"
if [[ $bootstrap_db != "$runtime_db" ]]; then
  [[ $bootstrap_db != "$runtime_db/"* && $runtime_db != "$bootstrap_db/"* ]] \
    || fail 'bootstrap and target runtime rpmdb paths overlap'
fi
for protected_path in "$bootstrap_db" "$runtime_db"; do
  [[ $staging_db != "$protected_path" \
     && $staging_db != "$protected_path/"* \
     && $protected_path != "$staging_db/"* ]] \
    || fail 'target staging rpmdb path overlaps a protected database path'
done

[[ -d $bootstrap_db && ! -L $bootstrap_db ]] \
  || fail 'the recorded bootstrap rpmdb directory is missing or unsafe'
[[ -n $(find "$bootstrap_db" -mindepth 1 -maxdepth 1 -print -quit) ]] \
  || fail 'the recorded bootstrap rpmdb directory is empty'
[[ ! -L $runtime_db ]] || fail 'the target runtime rpmdb path is a symlink'
[[ ! -e $staging_db ]] || fail 'target staging rpmdb path is not clean'
install -d -m 0700 "$staging_db"
rpmdb --dbpath "$staging_db" --importdb < "$transport"
rpmdb --dbpath "$staging_db" --verifydb

staging_manifest=$(mktemp)
runtime_manifest=$(mktemp)
trap 'rm -f -- "$staging_manifest" "$runtime_manifest"' EXIT
"$manifest_helper" --dbpath "$staging_db" >"$staging_manifest"
[[ -s $staging_manifest ]] || fail 'target RPM imported an empty package database'
cmp -s -- "$baseline_root/rpm-manifest.tsv" "$staging_manifest" \
  || fail 'target RPM import differs from the signed bootstrap transaction or header-digest manifest'

runtime_parent=${runtime_db%/*}
[[ -n $runtime_parent ]] || runtime_parent=/
[[ -d $runtime_parent && ! -L $runtime_parent ]] \
  || fail 'the target runtime rpmdb parent is missing or unsafe'
if [[ -e $runtime_db ]]; then
  [[ -d $runtime_db && ! -L $runtime_db ]] \
    || fail 'the target runtime rpmdb path is not a regular directory'
  [[ -z $(find "$runtime_db" -mindepth 1 -maxdepth 1 -print -quit) ]] \
    || fail 'the target runtime rpmdb path is unexpectedly nonempty'
fi
[[ $(stat -c '%d' -- "$staging_db") == "$(stat -c '%d' -- "$runtime_parent")" ]] \
  || fail 'target staging and runtime rpmdb paths are not on one filesystem'
if [[ -d $runtime_db ]]; then
  rmdir "$runtime_db"
fi
chmod 0755 "$staging_db"
mv -- "$staging_db" "$runtime_db"
"$manifest_helper" >"$runtime_manifest"
[[ -s $runtime_manifest ]] || fail 'target runtime RPM database is empty after import'
cmp -s -- "$baseline_root/rpm-manifest.tsv" "$runtime_manifest" \
  || fail 'target runtime RPM manifest differs after database placement'
rpmdb --verifydb

if [[ $bootstrap_db != "$runtime_db" ]]; then
  find "$bootstrap_db" -mindepth 1 -delete
  rmdir "$bootstrap_db"
fi
printf 'target rpmdb finalization: portable header-list import verified\n'
