<!-- SPDX-License-Identifier: Apache-2.0 -->
# npth

This directory packages the official stable nPth `1.8` release for openEuler
24.03 LTS SP3 on `riscv64`/RVA23. The GnuPG archive is pinned by SHA-256
`8bd24b4f23a3065d6e5b26e98aba9ce783ea4fd781069c1b35d149694e90ca3e`.
Its 63 members have one `npth-1.8` root and no absolute path, parent traversal,
symlink, or hardlink. Upstream also publishes a detached signature; SHA-256
remains the source contract because the review host had no OpenPGP verifier.

Snapshot `discovery-20260808T165000Z-9a89920c269462cd` freezes Arch core
`1.8-1`, AUR `android-riscv64-npth` `1.8-1`, Debian stable `1.8-3`, Fedora 44
GA `1.8-4.fc44`, openSUSE Tumbleweed `1.8-2.5`, and Ubuntu 26.04 LTS
`1.8-3build1`. The AUR row is metadata-only corroboration; no PKGBUILD or
distribution spec was executed. The independently reviewed official index
confirms stable `1.8`.

The fixed target repodata contains the declared `gcc` and `make` build
requirements. `%check` runs the complete upstream scheduling, signal, mutex,
condition, select, and timing suite. The installed smoke test creates and
joins a real nPth thread. No downstream or RISC-V patch is currently required.
RISC-V status remains `unknown` until the locked QEMU CI image runs.

External source licenses remain those of upstream. Apache-2.0 covers only the
original packaging metadata, test, and documentation in this directory.
