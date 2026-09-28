<!-- SPDX-License-Identifier: Apache-2.0 -->
# libgfshare

This directory packages libgfshare 2.0.0 for openEuler 24.03 LTS SP3 on
`riscv64`/RVA23. The official upstream tag resolves to immutable commit
`da0566422af4e0ad5c9e17cfe21f563e4274338d`; its HTTPS archive is pinned
by SHA-256. Upstream `COPYRIGHT` and the C source headers grant MIT terms.

The tag archive contains Autotools inputs rather than generated build files;
the package regenerates them in `%build`. `%check` retains all three upstream
Automake tests: finite-field verification, blockwise sharing, and CLI
split/combine. Installed smoke checks a two-of-three share roundtrip and
compiles and links against the packaged C API. These checks do not by
themselves prove native RISC-V hardware behavior or repository publication.
The repository's Apache-2.0 license covers original packaging files only.
