<!-- SPDX-License-Identifier: Apache-2.0 -->
# libdate-jd-perl

This directory packages upstream `https://metacpan.org/dist/Date-JD` version `0.006` for openEuler 24.03 LTS SP3 on `riscv64`/RVA23.

External source and patch licenses remain those of their respective upstream projects. The repository license only covers original packaging metadata, scripts, and documentation.

The official CPAN archive matches signed PAUSE checksums and the identical
Debian stable original. The author's original notice and both full Perl
license texts are installed.

The original three tests run unmodified with Math::BigRat and both POD
checkers available. Math::BigRat is also a runtime dependency so installed
users can rely on exact rational Julian-date conversion; smoke exercises
both scalar and rational results.
