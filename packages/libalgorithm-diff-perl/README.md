<!-- SPDX-License-Identifier: Apache-2.0 -->
# libalgorithm-diff-perl

This package maps the frozen inventory's exact `libalgorithm-diff-perl` key
to the official [Algorithm-Diff 1.201](https://metacpan.org/dist/Algorithm-Diff)
CPAN release. The official CPAN `CHECKSUMS` SHA-256 and an independent HTTPS
download agree on `0022da5982645d9ef0207f3eb9ef63e70e9713ed2340ed7b3850779b0d842a7d`.
The archive has one top-level tree, only regular files and directories, and
no traversal paths. CI verifies the pinned source before building for
openEuler 24.03 LTS SP3 `riscv64`/RVA23.

The module POD explicitly grants distribution under the same GPL/Artistic
choice as Perl. CPAN's generated `META.json` labels the license `unknown`
because `Makefile.PL` specifies a license URL rather than an SPDX key; that
metadata limitation is not being represented as an upstream license denial.

Upstream ships exactly two `t/` test files, `base.t` and `oo.t`; `%check`
runs both with `make test`, without exclusions. The installed-RPM smoke
checks the version, longest common subsequence, edit differences, and the
legacy comparison callback interface. Upstream deliberately does not install
the four `bin/` example scripts (`EXE_FILES` is omitted in `Makefile.PL`),
so this RPM preserves that choice. Target QEMU tests do not constitute native
RISC-V performance validation. CI build artifacts are not evidence of public
RPM repository publication.
