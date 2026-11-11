<!-- SPDX-License-Identifier: Apache-2.0 -->
# libcarp-assert-more-perl

This directory packages upstream `https://metacpan.org/dist/Carp-Assert-More` version `2.9.0` for openEuler 24.03 LTS SP3 on `riscv64`/RVA23.

External source and patch licenses remain those of their respective upstream projects. The repository license only covers original packaging metadata, scripts, and documentation.

The authorized official CPAN source SHA-256 is
`cdf7d445a2caeb55ff0a3f92f3b0f6d589a0bab935bb6028792e7e1261b48b14`.
It matches the publisher CHECKSUMS signature at its signing time.
Debian stable 2.9.0-1 establishes naming lineage only.

The original module and README retain Andy Lester's Artistic License
2.0 grant. The complete license text from the fixed SPDX commit is
installed alongside the original README.

The original MakeMaker default tests are unchanged. The recipe includes
the actual DateTime, Test::Exception, and both POD test providers so
the corresponding tests run. Installed smoke checks that a valid
integer is accepted and invalid input raises the expected assertion.
