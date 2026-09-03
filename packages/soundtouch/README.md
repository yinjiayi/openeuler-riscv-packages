<!-- SPDX-License-Identifier: Apache-2.0 -->
# soundtouch

This directory packages SoundTouch 2.4.1 for openEuler 24.03 LTS SP3 on
riscv64/RVA23. Arch stable, AUR metadata, and openSUSE Tumbleweed confirm
2.4.1; Fedora 44 GA, Debian stable, and Ubuntu GA provide the reviewed 2.4.0
baseline. AUR was queried only through read-only RPC for lib32-soundtouch
metadata. No PKGBUILD, install hook, patch, source instruction, or command from
AUR was read or executed.

The official Codeberg 2.4.1 tag archive was downloaded independently and
SHA-256 pinned. It has one soundtouch root, no absolute or parent-traversal
path, and no special entry. Its one symlink is an internal Lazarus test link to
a sibling build directory; it remains within the archive root and is not part
of the CMake build or installed files. The openEuler target currently carries
SoundTouch 2.3.1 with libSoundTouch.so.2, and upstream 2.4.1 retains SONAME 2.

Upstream 2.4.1 ships no automated test target: bin/run_test depends on an
author-local external audio directory and is not a self-contained suite. The
SPEC therefore adds deterministic soundstretch and public C++ API checks rather
than claiming or skipping a nonexistent runnable suite. The installed smoke
test repeats both checks against the packaged library and pkg-config metadata.
The target repository contains cmake, gcc-c++, and make for riscv64. RISC-V
status remains unknown until the pinned openEuler RVA23/QEMU workflow completes.

External source licenses remain upstream's. Apache-2.0 covers only this
repository's original packaging metadata, scripts, tests, and documentation.
