<!-- SPDX-License-Identifier: Apache-2.0 -->
# allegro

This directory packages Allegro 5.2.11.3 for openEuler 24.03 LTS SP3 on
`riscv64`/RVA23.  Allegro 5 is ABI- and source-incompatible with Allegro 4;
this provider installs only the versioned Allegro 5 libraries and the
`allegro*-5` pkg-config modules.

The fixed target repository provides every declared build dependency.  The
build keeps the core library and audio, image, font, TTF, color, memfile,
PhysicsFS, primitives, native-dialog, and video add-ons.  Optional FreeImage,
DUMB, OpenMPT, and minimp3 codec integration is disabled because the fixed
repository has no matching development provider.  The official release
archive is immutable in `sources.yaml` through its SHA-256 digest.

The upstream graphical test driver needs an active display, which target QEMU
CI does not provide.  `%check` instead builds and executes upstream's
display-independent internal list test.  Installed-RPM smoke verifies every
enabled pkg-config module and links a public API probe across all enabled
add-ons without opening a display.

The downstream patch makes generated pkg-config linker paths use
`CMAKE_INSTALL_LIBDIR`, matching the riscv64 `lib64` installation directory.
External source and patch licenses remain those of their respective upstream
projects; the repository license covers only original packaging metadata,
scripts, and documentation.
