<!-- SPDX-License-Identifier: Apache-2.0 -->
# patchelf

This directory packages PatchELF `0.19.1` for openEuler 24.03 LTS SP3 on
`riscv64`/RVA23. The official immutable versioned release asset is
independently SHA-256 pinned and passed single-root, path, link, and
special-entry safety inspection. Committed snapshot
`discovery-20260808T165000Z-9a89920c269462cd` is the immutable source of the
manifest lineage: it recorded Arch `0.19.1-1`, Debian `0.18.0-1.4`, Fedora
`0.18.0-9.fc43`, openSUSE `0.19.1-1.1`, and Ubuntu
`0.18.0-1.4build1` at `2026-08-08T16:50:00Z`. The current official 0.19.1
release verification is a separate hard gate, not a rewritten snapshot row.

AUR metadata was captured by the discovery run, but the committed canonical
PatchELF component contains no AUR lineage row. No PKGBUILD or distribution
spec was executed. The release tarball contains generated Autotools inputs, so the offline build
does not regenerate them. The complete upstream suite remains enabled and
exercises ELF headers, dynamic strings, RPATH, interpreters, dependencies,
symbol rewriting, malformed inputs, and cross-endian fixtures. Installed smoke
compiles an ELF executable, rewrites its RPATH, verifies its interpreter, and
runs the modified program.

External source licenses remain those of upstream. Apache-2.0 covers only the
original packaging metadata, scripts, tests, and documentation in this repo.
