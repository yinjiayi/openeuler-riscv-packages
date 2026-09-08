<!-- SPDX-License-Identifier: Apache-2.0 -->
# checksec

This directory packages the Fedora 44 GA `checksec` baseline, upstream version `2.7.1`, for openEuler 24.03 LTS SP3 on `riscv64`/RVA23. This is deliberately not described as the latest upstream stable version.

Fedora 44 dist-git was reviewed as text and was not executed. The official upstream 2.7.1 tag archive is pinned independently by SHA-256. The package installs the noarch shell implementation, disables its network self-update command, and runs a non-privileged ELF file check under the offline QEMU gate; Fedora's root/kernel test modes are not used as evidence for target-kernel behavior.

Upstream 3.2.0 is the latest detected release, but it requires Go 1.25 and does not vendor its module graph. The fixed openEuler 24.03 LTS SP3 repository provides Go 1.21.4, and package builds prohibit network access. A future 3.x update must first pin all module bytes and provide a compatible, audited target toolchain; until then 2.7.1 is the reproducible Fedora 44 fallback requested for this cohort.

External source and patch licenses remain those of their respective upstream projects. The repository license only covers original packaging metadata, scripts, and documentation.
