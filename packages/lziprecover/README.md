<!-- SPDX-License-Identifier: Apache-2.0 -->
# lziprecover

This directory packages lziprecover `1.26` for openEuler 24.03 LTS SP3 on
`riscv64`/RVA23. The official Savannah release archive is pinned by SHA-256,
is single-rooted, contains only regular files and directories, and includes
the upstream GPL-2.0-or-later license and all recovery test fixtures.
The pinned source and update metadata use Savannah's official direct download
mirror because the mirror-selection endpoint can intermittently return HTTP
502 while selecting a downstream mirror.

Frozen Debian, Fedora 44, openSUSE, and Ubuntu metadata corroborates the
component and stable release line. It was used only as read-only catalog
evidence; no distribution recipe was read or executed. The target repository
has no lziprecover package or provider. The separate lzip package's source,
installed manifest, and Provides do not contain `lziprecover`.

`%check` runs the complete upstream script covering decompression, malformed
input, byte repair, forward-error correction, merging, reproduction, splitting,
damaged-region extraction, and trailing-data handling. A clean local build ran
the full suite successfully with the official lzip 1.26 dependency. Installed
smoke verifies the version and decodes a fixed lzip stream; target SP3/RVA23 CI
remains authoritative.

The openEuler SP3 RISC-V binutils 2.42 linker reports an
`R_RISCV_PCREL_HI20` overflow while relaxing the PIE link. The SPEC disables
RISC-V linker relaxation for this small executable while retaining the
distribution compile and link hardening flags. Remove the workaround after the
target linker can build the package with relaxation enabled.

External source licenses remain those of upstream. Apache-2.0 covers only the
original packaging metadata, scripts, tests, and documentation here.
