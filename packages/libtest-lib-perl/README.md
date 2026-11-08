<!-- SPDX-License-Identifier: Apache-2.0 -->
# perl-test-lib

This directory packages upstream `https://metacpan.org/dist/Test-Lib` version `0.003` for openEuler 24.03 LTS SP3 on `riscv64`/RVA23.

External source and patch licenses remain those of their respective upstream projects. The repository license only covers original packaging metadata, scripts, and documentation.

The fixed CPAN archive SHA-256 matches MetaCPAN and signed PAUSE CHECKSUMS.
The original LICENSE retains Graham Knop's same-Perl terms. Fedora 44 GA
is discovery lineage, not a substitute source.

The build requires the release's verified META.yml before Makefile.PL so
the upstream maintainer-only Distar bootstrap is never entered. All seven
unchanged recursive tests run. Installed smoke finds a private fixture
from a nested test file; the package installs only the canonical manpage.
