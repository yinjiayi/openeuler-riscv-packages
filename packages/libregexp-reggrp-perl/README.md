<!-- SPDX-License-Identifier: Apache-2.0 -->
# libregexp-reggrp-perl

This directory packages upstream `https://metacpan.org/dist/Regexp-RegGrp` version `2.01` for openEuler 24.03 LTS SP3 on `riscv64`/RVA23.

External source and patch licenses remain those of their respective upstream projects. The repository license only covers original packaging metadata, scripts, and documentation.

The signed official CPAN 2.01 release is newer than Debian stable's
1.002001 packaging of the same module. The original copyright notice and
both full Perl license texts are installed.

All five original test files run unchanged, including POD validation.
Installed smoke checks copying and in-place substitutions, and verifies that
dynamic embedded Perl code is rejected on the supported modern Perl.
This package requires Perl 5.10 or newer, outside the source's legacy
`re eval` compatibility branch.
