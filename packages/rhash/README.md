<!-- SPDX-License-Identifier: Apache-2.0 -->
# rhash

This directory packages RHash `1.4.6` for openEuler 24.03 LTS SP3 on
`riscv64`/RVA23. Fedora 44 GA and Debian stable supplied reviewed `1.4.5`
baselines; the selected official stable release is corroborated by Arch
stable, openSUSE Tumbleweed, and Ubuntu 26.04 LTS GA.

Two independent downloads of the official stable tag produced the pinned
SHA-256. Archive inspection found one expected root, no absolute or
parent-traversal path, no link, and no special entry. The AUR search returned
only the VCS `rhash-git` lineage, which is not stable-release evidence and was
excluded. No AUR recipe or distribution spec was read or executed.

The network-free `%check` runs the upstream source-consistency check, the full
command-line suite, and both static and shared LibRHash suites. The installed
smoke test computes SHA-256 through both the CLI and the public library API.
The package's RISC-V status remains `unknown` until the pinned openEuler
RVA23/QEMU CI completes.

External source licenses remain upstream's. Apache-2.0 covers only this
repository's original packaging metadata, scripts, and documentation.
