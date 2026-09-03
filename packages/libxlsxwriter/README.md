<!-- SPDX-License-Identifier: Apache-2.0 -->
# libxlsxwriter

This directory packages upstream libxlsxwriter 1.2.4 for openEuler 24.03 LTS
SP3 on `riscv64`/RVA23. CI downloads the official release tag over HTTPS
and verifies its pinned SHA-256 before the network-enabled target build.

The package builds a shared library and enables the complete bundled C unit
and Python-driven functional suites. The installed-RPM smoke test compiles
against `xlsxwriter.pc`, creates a workbook containing text and numeric data,
and verifies the resulting XLSX ZIP signature. A package-local CMake patch
keeps the generated pkg-config libdir aligned with GNUInstallDirs.

External source licenses remain BSD, Zlib, MPL-2.0, MIT, and public-domain
terms as documented in `License.txt`; the downstream patch remains
BSD-2-Clause. The repository license only covers original packaging metadata,
scripts, and documentation.
