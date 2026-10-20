#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -Eeuo pipefail

fail() {
  printf 'target verification failed: %s\n' "$*" >&2
  exit 1
}

[[ $(uname -m) == riscv64 ]] || fail "uname -m is $(uname -m), expected riscv64"
[[ $(rpm -E '%{_arch}') == riscv64 ]] || fail "RPM macro architecture is not riscv64"
grep -Eqi '24\.03.*LTS.*SP3|24\.03-LTS-SP3' /etc/openEuler-release \
  || fail "/etc/openEuler-release is not 24.03 LTS SP3"

manifest=/usr/share/openeuler-riscv-ci/rpm-manifest.tsv
repomd=/usr/share/openeuler-riscv-ci/repomd.xml
manifest_helper=/usr/local/libexec/openeuler-riscv-ci/rpm-manifest.sh
official_repo=/etc/yum.repos.d/openeuler-rva23.repo
official_dnf_cache=/var/cache/dnf
cache_transaction=/usr/share/openeuler-riscv-ci/official-dnf-cache-transaction.json
[[ -s $manifest && -s $repomd ]] || fail "rootfs evidence is incomplete"
[[ -x $manifest_helper && ! -L $manifest_helper ]] \
  || fail "shared RPM manifest helper is missing or unsafe"
[[ -f $official_repo && ! -L $official_repo ]] \
  || fail "official repository configuration is missing or unsafe"
grep -Fqx 'gpgcheck=1' "$official_repo" \
  || fail "official repository RPM signature verification is not enabled"
grep -Fqx 'repo_gpgcheck=0' "$official_repo" \
  || fail "official repository metadata trust policy changed"
grep -Fqx 'metadata_expire=never' "$official_repo" \
  || fail "official repository cache is not immutable-image scoped"
grep -Fqx 'skip_if_unavailable=0' "$official_repo" \
  || fail "official repository cannot be skipped"
[[ -d $official_dnf_cache && ! -L $official_dnf_cache \
   && -n $(find "$official_dnf_cache" -mindepth 1 -print -quit) ]] \
  || fail "target DNF metadata cache is missing or unsafe"
[[ -f $cache_transaction && ! -L $cache_transaction ]] \
  || fail "target DNF metadata-cache transaction evidence is missing or unsafe"
sha256sum --check <(printf '%s  %s\n' "$(cat /usr/share/openeuler-riscv-ci/repomd.sha256)" "$repomd")
sha256sum --check <(printf '%s  %s\n' "$(cat /usr/share/openeuler-riscv-ci/rpm-manifest.sha256)" "$manifest")

python3 - "$cache_transaction" <<'PY'
import json
import sys

with open(sys.argv[1], encoding="utf-8") as handle:
    evidence = json.load(handle)
expected_command = [
    "dnf",
    "--setopt=retries=20",
    "--setopt=timeout=60",
    "--setopt=minrate=1000",
    "--setopt=max_parallel_downloads=1",
    "-y",
    "--disablerepo=*",
    "--enablerepo=openeuler-rva23",
    "makecache",
]
attempts = evidence.get("attempts")
if (
    evidence.get("kind") != "dnf-transaction"
    or evidence.get("status") != "passed"
    or evidence.get("exit_code") != 0
    or evidence.get("command") != expected_command
    or evidence.get("budget_seconds") != 7300
    or evidence.get("attempt_timeouts_seconds") != [4200, 3000]
    or not isinstance(attempts, list)
    or not attempts
    or attempts[-1].get("exit_code") != 0
):
    raise SystemExit("target DNF metadata-cache transaction evidence is invalid")
PY

[[ -z $(find "$official_dnf_cache" -type f -name '*.rpm' -print -quit) ]] \
  || fail "target DNF cache unexpectedly contains RPM payloads"
# DNF 4.16 loads official primary and filelists metadata for every repository
# sack.  Cache-only loading therefore proves that the immutable image contains
# the target DNF cache without allowing this verification step any network use.
dnf --cacheonly --quiet --disablerepo='*' --enablerepo=openeuler-rva23 \
  list bash >/dev/null \
  || fail "target DNF cannot load the official repository from image metadata cache"

live_manifest=$(mktemp)
trap 'rm -f -- "$live_manifest"' EXIT
"$manifest_helper" >"$live_manifest"
[[ -s $live_manifest ]] || fail "target runtime RPM database is empty"
for anchor in bash rpm rpm-build gcc gcc-c++ make python3; do
  awk -F '\t' -v anchor="$anchor" '$1 == anchor { found=1 } END { exit !found }' \
    "$live_manifest" \
    || fail "target runtime RPM database is missing fixed anchor $anchor"
done
cmp -s -- "$manifest" "$live_manifest" \
  || fail "target runtime RPM manifest differs from the embedded bootstrap manifest"

/usr/local/bin/rva23-selftest || fail "representative RVA23 instructions did not execute"
printf 'target verification: openEuler 24.03 LTS SP3 riscv64/RVA23 pass\n'
