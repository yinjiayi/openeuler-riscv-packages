<!-- SPDX-License-Identifier: Apache-2.0 -->
# jbigkit

This directory packages JBIG-KIT 2.1 for openEuler 24.03 LTS SP3 on
riscv64/RVA23. Fedora 44, Arch stable, Debian stable, openSUSE Tumbleweed, and
Ubuntu all independently retain the upstream 2.1 release. AUR was queried only
through its read-only RPC for android-riscv64-jbigkit metadata; no PKGBUILD,
install hook, patch, or command from AUR was read or executed.

The official University of Cambridge release archive is pinned by SHA-256.
Archive inspection found one jbigkit-2.1 root and no absolute path, parent
traversal, link, or special entry. The SPEC builds both shared libraries
directly from the unmodified upstream objects, with the established
libjbig.so.2.1 and libjbig85.so.2.1 SONAMEs already present on the openEuler
target.

The complete upstream `make test` gate remains enabled. It covers the library
T.82/T.85 codec tests and the PBM/JBIG functional round trips and passed in a
fresh host preflight. The installed smoke test adds a public API link check and
a PBM-to-JBIG-to-PBM conversion against the packaged shared libraries. RISC-V
status remains unknown until the pinned openEuler RVA23/QEMU workflow
completes.

External source licenses remain upstream's. Apache-2.0 covers only this
repository's original packaging metadata, scripts, tests, and documentation.
