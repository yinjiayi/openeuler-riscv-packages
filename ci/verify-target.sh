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
[[ -s $manifest && -s $repomd ]] || fail "rootfs evidence is incomplete"
sha256sum --check <(printf '%s  %s\n' "$(cat /usr/share/openeuler-riscv-ci/repomd.sha256)" "$repomd")
sha256sum --check <(printf '%s  %s\n' "$(cat /usr/share/openeuler-riscv-ci/rpm-manifest.sha256)" "$manifest")

/usr/local/bin/rva23-selftest || fail "representative RVA23 instructions did not execute"
printf 'target verification: openEuler 24.03 LTS SP3 riscv64/RVA23 pass\n'

