<!-- SPDX-License-Identifier: Apache-2.0 -->
# perl-package-new

This directory packages upstream `https://metacpan.org/dist/Package-New` version `0.10` for openEuler 24.03 LTS SP3 on `riscv64`/RVA23.

External source and patch licenses remain those of their respective upstream projects. The repository license only covers original packaging metadata, scripts, and documentation.

- Signed CPAN 0.10, corroborated by the exact-source Fedora 44 GA package 0.10-3.fc44. The original BSD-3-Clause LICENSE is installed verbatim.
- The unchanged default MakeMaker suite runs four files, 51 assertions. It tests object construction, dumping, and the deliberate no-Data::Dumper fallback.
- Test::Simple and Devel::Hide are build-only. Data::Dumper is present for the positive build tests and remains optional in the upstream runtime; the installed smoke exercises whichever branch is available.
