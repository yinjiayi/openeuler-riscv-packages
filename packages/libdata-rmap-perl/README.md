<!-- SPDX-License-Identifier: Apache-2.0 -->
# Data::Rmap 0.65

This package maps the frozen Ubuntu `libdata-rmap-perl` key to the official
[Data-Rmap 0.65](https://metacpan.org/dist/Data-Rmap) CPAN release. The
publisher's author-directory `CHECKSUMS` and an independent HTTPS download
agree on SHA-256 `d076317d29365420a06223b1638451dc012ce2ae77d56c7a9a25bb378953dcf3`.
The archive has one top-level tree, regular files and directories only, and
no traversal paths. The copyright holder's sole installed module POD grants
redistribution under the same GPL/Artistic terms as Perl; no bundled file
asserts a conflicting license. CI verifies the pinned source before building.

The official openEuler 24.03 LTS SP3 riscv64/RVA23 primary has neither a
`perl-Data-Rmap` RPM nor a `perl(Data::Rmap)` provider. It uniquely supplies
Scalar::Util, Data::Dumper, Test::Exception, Test::More and MakeMaker. The
upstream-generated Makefile.PL is used instead of Build.PL's unused
author-only Debian action; this leaves upstream source and tests unchanged.

The sole default upstream test file passed all 39 local assertions without
skips. Exact-head target CI must prove the target build, intact test run and
installed-RPM functional smoke. PR CI products do not establish public RPM
publication.
