<!-- SPDX-License-Identifier: Apache-2.0 -->
# cunit

This directory packages the official CUnit 2.1-3 release as RPM version
`2.1.3` for openEuler 24.03 LTS SP3 on `riscv64`/RVA23.

The SourceForge release archive is pinned by SHA-256 in `sources.yaml` and
was inspected for a single safe archive root. The package builds the shared
library, automated/basic/console interfaces, headers, pkg-config metadata,
manual page, and upstream XML support files. CUnit's internal test program
remains enabled and is run during `%check`; the installed smoke test also
compiles and runs a small basic-interface test without network access.

The upstream source is covered by the GNU Library General Public License
version 2. The repository license covers only the original packaging metadata,
test, and documentation files.
