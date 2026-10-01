<!-- SPDX-License-Identifier: Apache-2.0 -->
# libansilove

This directory packages libansilove 1.4.2 for openEuler 24.03 LTS SP3
`riscv64`/RVA23. The official [latest release](https://github.com/ansilove/libansilove/releases/tag/1.4.2)
provides a 62,575-byte source asset, downloaded over HTTPS and pinned to
SHA-256 `8bd4d0775ff558aacfebd7e7e284baa96d781183bf767283bf8410f44a2e2434`.
All 89 archive entries are regular files or directories beneath the expected
release root, with no traversal. The upstream `LICENSE` and public header
identify BSD-2-Clause terms.

The frozen discovery snapshot records Debian 1.4.1 and Ubuntu 1.4.2; the
official release is the source of truth here. The target repository provides
the GD development package used by the CMake build. Upstream supplies no
executable test suite, so `%check` and the installed smoke test each render a
small ANSI fixture through the public API and verify the PNG magic bytes.
Neither test needs a display, graphics device, or privileged operation.
RISC-V compilation and installation remain unverified until CI runs.
