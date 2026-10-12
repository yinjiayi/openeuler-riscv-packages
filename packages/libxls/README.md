<!-- SPDX-License-Identifier: Apache-2.0 -->
# libxls

This directory packages the official libxls 1.6.3 release for openEuler 24.03
LTS SP3 on `riscv64`/RVA23. Its source archive is SHA-256 pinned in
`sources.yaml`; network retrieval during the target build is permitted, but
the downloaded bytes must match that digest before `rpmbuild`.

`%check` runs upstream's registered `test_libxls` suite with `make check`, then
its additional C and C++ test programs against the included `test2.xls`
fixture. The installed-package smoke checks the public API, pkg-config data,
and `xls2csv` handling of a missing workbook. CI build and installation smoke
results are not evidence of repository publication or native RISC-V testing.

The upstream source license is BSD-2-Clause. The repository's Apache-2.0
license applies only to original packaging files.
