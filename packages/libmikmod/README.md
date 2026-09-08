<!-- SPDX-License-Identifier: Apache-2.0 -->
# libmikmod

This directory packages libmikmod 3.3.13 for openEuler 24.03 LTS SP3 on
riscv64/RVA23. Fedora 44, Arch stable, Debian stable, openSUSE Tumbleweed, and
Ubuntu all independently track the 3.3.13 source line. AUR was queried only
through its read-only RPC for related mikmod player metadata; no PKGBUILD,
install hook, patch, or command from AUR was read or executed.

The official SourceForge 3.3.13 release asset is pinned by SHA-256. Archive
inspection found one libmikmod-3.3.13 root and no absolute path, parent
traversal, link, or special entry. The source's LP64 detection recognizes the
RVA23 compiler's `__LP64__` definition, and the installed libmikmod.so.3 ABI
major matches openEuler's existing library.

The SPEC invokes the upstream make check target unchanged. This release does
not register standalone cases under that target, so the installed smoke test
also exercises version and loader registration through the public C API. A
fresh macOS compile preflight stopped at a Darwin-only libtool visibility/link
interaction; it is not target evidence and is not used as a waiver. RISC-V
status remains unknown until the pinned openEuler RVA23/QEMU workflow
completes.

External source licenses remain upstream's. Apache-2.0 covers only this
repository's original packaging metadata, scripts, tests, and documentation.
