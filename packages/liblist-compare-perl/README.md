<!-- SPDX-License-Identifier: Apache-2.0 -->
# liblist-compare-perl

The frozen inventory's exact `liblist-compare-perl` key maps to official
stable [List-Compare 0.55](https://metacpan.org/dist/List-Compare). Its
official HTTPS archive SHA-256 is
`cc719479836579d52b02bc328ed80a98f679df043a99b5710ab2c191669eb837`,
identical to the publisher's `CHECKSUMS` entry. All 73 archive entries are
regular files or directories under one root, without traversal paths or
links. The bundled README grants the same terms as Perl itself; META.json
and Makefile.PL independently declare Perl terms, with no license conflict.

The official openEuler 24.03 LTS SP3 `riscv64`/RVA23 `everything` primary
metadata SHA-256 is
`fdb1663ee6c803e8efcc83c19b7a1548f047f08abba8a52f5fe623b222064d1a`.
It contains neither `perl-List-Compare` nor providers for its four module
files, and includes all declared Perl build/test dependencies. This is a
snapshot collision check, not a future guarantee.

`%check` retains all 52 default upstream test files (4,190 assertions passed
on local Perl 5.34.1). The installed-RPM smoke checks the object-oriented
and functional APIs and the generated module provider. Exact-head target CI
must still establish the SP3 RVA23 RPM build, complete suite, and installed
smoke; no local RPM/QEMU result is claimed.
