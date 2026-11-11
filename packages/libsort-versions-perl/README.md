<!-- SPDX-License-Identifier: Apache-2.0 -->
# perl-sort-versions

This directory packages upstream `https://metacpan.org/dist/Sort-Versions` version `1.62` for openEuler 24.03 LTS SP3 on `riscv64`/RVA23.

External source and patch licenses remain those of their respective upstream projects. The repository license only covers original packaging metadata, scripts, and documentation.

Sort::Versions retains its original LICENSE. The static portions of its
generated Makefile.PL match the exact Dist::Zilla::Plugin::MakeMaker 5.037
template. The notice-only patch adds the donor's original complete same-Perl
LICENSE with Ricardo SIGNES's copyright; it changes no code or upstream tests.
The original `make test` runs without filtering. The installed smoke checks
numeric version ordering through both the comparison and sort interfaces.
