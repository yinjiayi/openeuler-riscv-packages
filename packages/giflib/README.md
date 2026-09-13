<!-- SPDX-License-Identifier: Apache-2.0 -->
# giflib

This directory packages giflib 6.1.3 for openEuler 24.03 LTS SP3 on
riscv64/RVA23. Fedora 44 GA supplies the reviewed 6.1.2 baseline, while Arch
stable confirms the selected 6.1.3 official stable release. Debian stable,
openSUSE Tumbleweed, and Ubuntu GA retain the 5.2.2 line. AUR was queried only
through its read-only RPC for android-riscv64-giflib metadata; no PKGBUILD,
install hook, patch, or command from AUR was read or executed.

The official SourceForge release asset was downloaded independently and pinned
by SHA-256. Archive inspection found exactly one giflib-6.1.3 root and no
absolute path, parent traversal, link, or special entry. The openEuler target
currently provides giflib 5.2.2 with libgif.so.7; upstream 6.1.3 deliberately
retains that SONAME, so this update preserves the target ABI major.

The SPEC runs upstream's complete 51-case TAP regression suite with make check.
A macOS preflight reached 50 passing tests; its sole failure was the suite's
GNU head --bytes=-20 invocation, which BSD head does not implement. That
host-only result is not a target waiver: the unchanged full suite runs in the
Linux RVA23 build. The installed smoke test creates a GIF through the public C
API and reads it with giftext. RISC-V status remains unknown until the pinned
openEuler RVA23/QEMU workflow completes.

External source licenses remain upstream's. Apache-2.0 covers only this
repository's original packaging metadata, scripts, tests, and documentation.
