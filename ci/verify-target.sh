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
[[ -s $manifest && -s $repomd ]] || fail "rootfs evidence is incomplete"
[[ -x $manifest_helper && ! -L $manifest_helper ]] \
  || fail "shared RPM manifest helper is missing or unsafe"
sha256sum --check <(printf '%s  %s\n' "$(cat /usr/share/openeuler-riscv-ci/repomd.sha256)" "$repomd")
sha256sum --check <(printf '%s  %s\n' "$(cat /usr/share/openeuler-riscv-ci/rpm-manifest.sha256)" "$manifest")

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
