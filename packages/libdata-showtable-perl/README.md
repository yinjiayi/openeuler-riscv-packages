<!-- SPDX-License-Identifier: Apache-2.0 -->
# Data::ShowTable 4.6

The frozen Ubuntu `libdata-showtable-perl` 4.6-4 key maps to the official
[Data-ShowTable 4.6](https://metacpan.org/dist/Data-ShowTable) CPAN release.
The publisher's author-directory `CHECKSUMS` and an independent HTTPS
download agree on SHA-256
`8f8958b99b1480104f7cbde877a5204c5cc6990a00ded07886cb43eb72527ba3`.
Ubuntu's original archive MD5 also matches that publisher record. The
ordinary-file archive has one source tree and no traversal paths.

The release `Copyright` and `GNU-LICENSE` grant GPL version 2 or later;
`Makefile.PL`, the installed `ShowTable.pm`, and installed `showtable` command
repeat the same grant. The test fixtures and reference outputs are covered by
the release-wide grant; no bundled file states conflicting terms. The CLI
source internally says version 4.5, but the archive and module are 4.6; no
claim of a distinct CLI release is made.

The official openEuler 24.03 LTS SP3 riscv64/RVA23 primary has neither a
`perl-Data-ShowTable` RPM nor a `perl(Data::ShowTable)` provider. It uniquely
supplies Carp, Exporter, MakeMaker, and Test::Harness; `coreutils` and
`diffutils` supply the test commands. The full 22-file upstream suite keeps
all 161 bundled reference outputs and passes locally with no skips. Exact-head
target CI must confirm the full suite, RPM build, DNF install, installed CLI
rendering, and physical RPM/SRPM products. A green PR is not publication.
