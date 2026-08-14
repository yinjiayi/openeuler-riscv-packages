<!-- SPDX-License-Identifier: Apache-2.0 -->
# zlib-ng

This directory packages zlib-ng `2.3.3` for openEuler 24.03 LTS SP3 on
`riscv64`/RVA23. Fedora 44 GA, Arch stable, openSUSE Tumbleweed, and an
eligible non-bin AUR cross-toolchain metadata row all identify the same
stable release. Debian stable and Ubuntu 26.04 LTS GA had no zlib-ng source
row in the committed discovery snapshot; that absence is not presented as
corroboration.

Two independent downloads of the official stable tag produced the pinned
SHA-256. Archive inspection found one expected root, no absolute or
parent-traversal path, no link, and no special entry. AUR was queried through
metadata only; no AUR recipe or distribution spec was read or executed.

The build produces shared and static native-API libraries so upstream does
not auto-disable its GoogleTest suite in shared-only mode. System
`gtest-devel` avoids an unpinned test dependency, and `%check` runs every
configured CTest. `WITH_RVV=OFF` follows Fedora 44's explicit riscv64
toolchain boundary. The optional Zbc CRC path is also disabled because the
commit-bound openEuler QEMU run reached SIGILL after switching the full test
suite to the statically linked library. Generic CRC remains enabled and no
test is removed or ignored. The upstream fix merged as zlib-ng commit
`9f396c3d09d65dc59cce607d52f67f03b266c2de` remains backported so the source
tree has the accepted Zbc-without-RVV build fix when runtime Zbc support can
be safely re-enabled. The installed smoke test performs a real
compression/decompression round trip through `zlib-ng.h`. RISC-V status
remains `unknown` until pinned openEuler RVA23/QEMU CI completes.

External source licenses remain upstream's. Apache-2.0 covers only this
repository's original packaging metadata, scripts, and documentation.
