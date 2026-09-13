<!-- SPDX-License-Identifier: Apache-2.0 -->
# jpeginfo

This directory packages jpeginfo 1.7.1 for openEuler 24.03 LTS SP3 on
riscv64/RVA23. Fedora 44 GA, AUR metadata, Debian stable, openSUSE Tumbleweed,
and Ubuntu GA all identify jpeginfo 1.7.1. The frozen resolver grouped jpeginfo
with the same publisher's jpegoptim component; Arch stable contained only that
related jpegoptim package, not an exact jpeginfo package. The Arch row is
therefore retained as transparent publisher-family evidence and is not claimed
as jpeginfo version corroboration.

AUR was queried only through read-only RPC for jpeginfo metadata. No PKGBUILD,
install hook, patch, source instruction, or command from AUR was read or
executed. The source is the official non-draft, non-prerelease v1.7.1 GitHub
release tag archive, independently downloaded and SHA-256 pinned. Archive
inspection found one jpeginfo-1.7.1 root and no absolute path, parent traversal,
link, or special entry.

The network-free build keeps the complete upstream Python unittest suite,
including its bundled valid and deliberately damaged JPEG fixtures. The
installed smoke test verifies the version and the documented corrupt-input
error path. The target repository contains gcc, make, libjpeg-turbo-devel, and
python3 for riscv64. RISC-V status remains unknown until the pinned openEuler
RVA23/QEMU workflow completes.

External source licenses remain upstream's. Apache-2.0 covers only this
repository's original packaging metadata, scripts, tests, and documentation.
