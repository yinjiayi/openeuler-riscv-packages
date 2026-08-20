<!-- SPDX-License-Identifier: Apache-2.0 -->
# libxmp

This directory packages libxmp 4.7.2 for openEuler 24.03 LTS SP3 on
riscv64/RVA23. Fedora 44 GA provides the reviewed 4.6.3 baseline, while Arch
stable and openSUSE Tumbleweed track the selected 4.7.2 stable release. Debian
stable retains 4.6.2; Ubuntu's related xmp player lineage provides an
additional independently frozen cross-check. AUR was queried only through its
read-only RPC for xmp metadata; no PKGBUILD, install hook, patch, or command
from AUR was read or executed.

The official SourceForge 4.7.2 release asset is pinned by SHA-256. Its digest
also matches the checksum published for the upstream GitHub release asset.
Archive inspection found one libxmp-4.7.2 root and no absolute path, parent
traversal, link, or special entry. The package installs libxmp.so.4 and its
development interface; the ABI major is unchanged from Fedora 44's baseline.

The SPEC runs the complete regression target shipped in the release archive:
make check exercises the IT, ITZ, and XM fixtures. That suite passed in a
fresh host preflight. The installed smoke test then creates and frees a
decoder context through the public C API. RISC-V status remains unknown until
the pinned openEuler RVA23/QEMU workflow completes.

External source licenses remain upstream's. Apache-2.0 covers only this
repository's original packaging metadata, scripts, tests, and documentation.
