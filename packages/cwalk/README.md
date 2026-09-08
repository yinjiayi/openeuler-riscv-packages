<!-- SPDX-License-Identifier: Apache-2.0 -->
# cwalk

This directory packages upstream cwalk 1.2.9 for openEuler 24.03 LTS SP3 on
`riscv64`/RVA23. CI downloads the official tag archive over HTTPS and verifies
its pinned SHA-256 before building it.

The downstream CMake patch supplies the SONAME and target libdir metadata
required for a conventional RPM shared-library split. External source and
patch licenses remain MIT; the repository license covers only original
packaging metadata, scripts, and documentation.
