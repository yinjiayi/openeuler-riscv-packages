<!-- SPDX-License-Identifier: Apache-2.0 -->
# figlet

This directory packages FIGlet 2.2.5 for openEuler 24.03 LTS SP3 on
`riscv64`/RVA23. The official GitHub tag resolves to commit
`38518633367046425e63fc3328888352ccaae9a3`; its HTTPS archive is pinned
by SHA-256. The archive has no absolute/traversal paths or symlinks, and
upstream `LICENSE` grants BSD-3-Clause rights.

`%check` runs upstream `make check vercheck`: 26 font/rendering cases and
version-reference checks. Installed smoke verifies the reported version,
system font directory, and rendering with shipped fonts. These tests do not
by themselves prove native RISC-V hardware behavior or repository
publication. The repository's Apache-2.0 license covers original packaging
files only.
