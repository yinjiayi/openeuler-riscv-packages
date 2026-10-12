<!-- SPDX-License-Identifier: Apache-2.0 -->
# libcue

This directory packages the official libcue 2.3.0 release for openEuler
24.03 LTS SP3 on `riscv64`/RVA23. CI downloads the official GitHub release
tag over HTTPS and verifies its pinned SHA-256 before the network-enabled
target build.

The package builds the shared parser library and a development subpackage.
`%check` runs all six upstream CTest parser regressions. The installed-RPM
smoke test compiles against `libcue.pc`, parses an in-memory CUE sheet, and
checks its track mode and CD-TEXT title through the public API.

The upstream source combines GPL-2.0-only and BSD-2-Clause code. The
repository license covers only the original packaging metadata, scripts,
and documentation.
