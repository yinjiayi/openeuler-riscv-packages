<!-- SPDX-License-Identifier: Apache-2.0 -->
# libuecc

This directory packages libuecc v7 for openEuler 24.03 LTS SP3 on
`riscv64`/RVA23. The official v7 tag resolves to commit
`7c9a6f6af088d0764e792cf849e553d7f55ff99e`; the commit archive is
SHA-256 pinned and may be fetched during the target build. The upstream
`COPYRIGHT` file grants the BSD-2-Clause license.

The upstream CMake project registers no automated test suite. `%check`
verifies public-API base-point encoding, load/store, scalar multiplication,
doubling, addition, and inverse properties against the known Ed25519 base
encoding. The installed-package smoke independently compiles and links a
client through `pkg-config` and checks the same known encoding. These
functional checks do not establish cryptographic security, timing safety,
or native RISC-V performance. No privileged operation or network service
is required for the checks.

The repository's Apache-2.0 license covers original packaging metadata and
scripts only. A successful CI build does not establish repository publication
or native RISC-V validation.
