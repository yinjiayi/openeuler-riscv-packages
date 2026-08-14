<!-- SPDX-License-Identifier: Apache-2.0 -->
# uriparser

This directory packages uriparser `1.0.2` for openEuler 24.03 LTS SP3 on
`riscv64`/RVA23. Fedora 44 GA supplied the reviewed `1.0.0-2.fc44` baseline;
the selected official stable release is corroborated by Arch stable and
openSUSE Tumbleweed. Debian stable and Ubuntu 26.04 LTS GA remain on the
0.9.8 line.

Two independent downloads of the official stable release asset produced the
pinned SHA-256. Archive inspection found one expected root, no absolute or
parent-traversal path, no link, and no special entry. AUR RPC returned no
matching package; that absence is recorded and is not represented as version
corroboration. No AUR recipe or distribution spec was read or executed.

The network-free build enables the complete upstream GTest suite using the
openEuler `gtest-devel` package. Optional generated API documentation is not
part of this binary/development package and is disabled without weakening the
test suite. The installed smoke test parses an HTTPS URI with both `uriparse`
and the public C API. RISC-V status remains `unknown` until pinned openEuler
RVA23/QEMU CI completes.

External source licenses remain upstream's. Apache-2.0 covers only this
repository's original packaging metadata, scripts, and documentation.
