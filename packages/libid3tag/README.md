<!-- SPDX-License-Identifier: Apache-2.0 -->
# libid3tag

This directory packages libid3tag `0.16.4` for openEuler 24.03 LTS SP3 on
`riscv64`/RVA23. The official Codeberg tag resolves to commit
`fff52d4e27a6f8e3a714bd304e4258d9e1b0dad8`; its immutable-commit HTTPS
archive is SHA-256 pinned to
`2e9058af51e5f3881c13c55a9790abb9870812cc0f5917b6f3e825c6ae9b9f39`.
The archive has one root and only regular files and directories. `COPYRIGHT`
specifies GPL-2.0-or-later.

Upstream's CMake project produces the shared `libid3tag.so.0` library, public
header, pkg-config file, and CMake package configuration. It registers no
upstream test target. `%check` and installed-RPM smoke each compile a public
API consumer and verify an ID3v1 render/parse round trip. These focused tests
do not establish exhaustive ID3v2 compatibility.

Frozen Arch metadata supplies discovery lineage only; no distribution recipe
was executed. The upstream source keeps GPL-2.0-or-later terms; Apache-2.0
covers the original packaging metadata, tests, and documentation here.
