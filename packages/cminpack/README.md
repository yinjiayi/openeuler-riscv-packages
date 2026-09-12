<!-- SPDX-License-Identifier: Apache-2.0 -->
# cminpack

This directory packages CMinpack `1.3.14` for openEuler 24.03 LTS SP3 on
`riscv64`/RVA23. The annotated `v1.3.14` tag dereferences to immutable commit
`48c2b6ecd180ad134c626365e3092ba5dd5463a7`; its SHA-256-pinned archive is
single-rooted and contains no unsafe paths, links, or special members. The
archive contains the original MINPACK redistribution terms and every maintained
C, C++, precision-variant, fixture, and FORTRAN-reference cross-check test.

Read-only AUR RPC, Debian, Fedora 44 GA, and Ubuntu provide frozen lineage;
some distribution snapshots remain on older CMinpack versions while upstream
and the AUR component corroborate current 1.3.14. No AUR PKGBUILD or external
packaging recipe was read or executed. The target has no CMinpack package or
provider/consumer collision for the three new `libcminpack*.so.1` ABIs.

`%check` runs all 44 registered tests at single, double, and long-double
precision, including all committed FORTRAN-reference cross-checks. Python is a
hard BuildRequires so those reference gates cannot disappear. Installed smoke
verifies all three SONAMEs and compiles and runs the public double-precision API.

External source licenses remain those of upstream. `LicenseRef-Minpack`
identifies the bundled MINPACK terms without mapping them to a broader SPDX
license. Apache-2.0 covers only original packaging material here.
