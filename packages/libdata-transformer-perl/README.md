<!-- SPDX-License-Identifier: Apache-2.0 -->
# Data::Transformer 0.04

The frozen Ubuntu `libdata-transformer-perl` 0.04-3 key maps to the official
[Data-Transformer 0.04](https://metacpan.org/dist/Data-Transformer) CPAN
release. The publisher's author-directory `CHECKSUMS` and an independent
HTTPS download agree on the 13,579-byte archive SHA-256
`8223c9feca78d094f45cc07f491855919d8499c53c4b424679eca19b8dc747bb`.
Ubuntu's original archive MD5 agrees with the same publisher record.

Copyright holder Baldur Kristinsson explicitly permits redistribution under
Perl's terms in the sole installed module POD and release README. The bundled
`LICENSE` spells out GPL version 1 or later, or Artistic 1.0. No file in the
ordinary-file source archive states conflicting terms.

The official openEuler 24.03 LTS SP3 riscv64/RVA23 primary has neither a
`perl-Data-Transformer` RPM nor a `perl(Data::Transformer)` provider. It
uniquely supplies Test::Simple 1.302198 (upstream requires at least 0.44),
MakeMaker, and Test::Harness. The sole default upstream test file remains
unchanged and passes all 29 assertions locally without skips. Exact-head
target CI must confirm the full suite, RPM build, DNF installation, installed
traversal smoke, and physical RPM/SRPM products. PR CI does not establish
public RPM publication.
