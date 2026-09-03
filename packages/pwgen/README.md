<!-- SPDX-License-Identifier: Apache-2.0 -->
# pwgen

This directory packages pwgen 2.08 for openEuler 24.03 LTS SP3 on
riscv64/RVA23. Arch stable, Debian stable, Fedora 44 GA, openSUSE Tumbleweed,
and Ubuntu GA all retain the 2.08 release. The frozen AUR lineage is
pwgen-static 2.08 metadata. AUR was queried only through read-only RPC; no
PKGBUILD, install hook, patch, source instruction, or command from AUR was read
or executed.

The official versioned SourceForge release asset was downloaded independently
and SHA-256 pinned, and its v2.08 tag is also visible in the official upstream
Git repository. Archive inspection found exactly one pwgen-2.08 root and no
absolute path, parent traversal, link, or special entry. GPL-2.0-only is stated
in the upstream source headers and in the copyright file bundled in the
official source archive.

Upstream 2.08 ships no test target or dedicated automated suite. The SPEC does
not invent a skipped suite: it adds deterministic checks for secure-mode output
shape and repeatability of the documented file-hash mode. The installed smoke
test generates multiple secure passwords and verifies their count and length.
The target repository contains all declared build requirements for riscv64.
RISC-V status remains unknown until the pinned openEuler RVA23/QEMU workflow
completes.

External source licenses remain upstream's. Apache-2.0 covers only this
repository's original packaging metadata, scripts, tests, and documentation.
