<!-- SPDX-License-Identifier: Apache-2.0 -->
# libtest-more-utf8-perl

`Test::More::UTF8` enables UTF-8 source text and UTF-8 test output for Perl
`Test::More`. This noarch package uses the official
[CPAN release](https://metacpan.org/dist/Test-More-UTF8) 0.05 for openEuler
24.03 LTS SP3 on `riscv64`/RVA23. The exact archive SHA-256 is pinned in
`sources.yaml`; [Debian stable](https://packages.debian.org/stable/libtest-more-utf8-perl)
provides discovery lineage. The original README contains the same-Perl
license notice and is installed unchanged. No source patch is needed.

The build runs offline and `%check` runs the original `make test`, including
both supplied POD documentation checks. Installed smoke verifies that the
module enables UTF-8 source text and emits the expected UTF-8 TAP assertion
and test count.

External source and patch licenses remain those of their respective upstream projects. The repository license only covers original packaging metadata, scripts, and documentation.
