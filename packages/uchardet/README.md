<!-- SPDX-License-Identifier: Apache-2.0 -->
# uchardet

This directory packages uchardet `0.0.8` for openEuler 24.03 LTS SP3 on
`riscv64`/RVA23. Fedora 44 GA, Arch stable, openSUSE Tumbleweed, Debian
stable, and Ubuntu 26.04 LTS GA independently identify the same stable release
line.

The independently calculated SHA-256 matches the checksum published in the
official release directory. Archive inspection found one expected root, no
absolute or parent-traversal path, no link, and no special entry. AUR RPC
returned only the VCS `uchardet-git` lineage, which was excluded as
pre-release evidence. No AUR recipe or distribution spec was read or
executed.

The network-free build retains all upstream CTest cases; only the five
known-broken encodings excluded by upstream's own CMake contract remain
upstream skips. The installed smoke test exercises both the CLI and public C
API on real ASCII input. The package's RISC-V status remains `unknown` until
the pinned openEuler RVA23/QEMU CI completes.

External source licenses remain upstream's. Apache-2.0 covers only this
repository's original packaging metadata, scripts, and documentation.
