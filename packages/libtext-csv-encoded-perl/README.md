<!-- SPDX-License-Identifier: Apache-2.0 -->
# libtext-csv-encoded-perl

The frozen inventory records Ubuntu `libtext-csv-encoded-perl` 0.25-4.
The official stable [CPAN Text-CSV-Encoded 0.25](https://metacpan.org/dist/Text-CSV-Encoded)
archive is pinned to SHA-256
`248a5983a20dd57786639e88dafdd654f3b93925490120d6d712da6b2be5b9d0`,
which matches publisher `CHECKSUMS`. All 46 archive entries remain within one
top-level directory and contain no links, special files or path traversal.
Its `LICENSE`, `README.pod` and all four Perl modules grant the same terms
as Perl 5: GPL-1.0-or-later or Artistic-1.0-Perl. The historical discovery
`license-blocked` flag predates review of this archive; it is not a build or
publication result.

The official openEuler 24.03 LTS SP3 RVA23 `everything` primary metadata,
SHA-256 `fdb1663ee6c803e8efcc83c19b7a1548f047f08abba8a52f5fe623b222064d1a`,
has no `perl-Text-CSV-Encoded` RPM or `perl(Text::CSV::Encoded)` provider.
It provides Text::CSV 2.04, its pure-Perl backend and Text::CSV_XS 1.48.
The SPEC installs both backends for the full upstream default test suite;
all 14 `t/*.t` files, including both backend branches and the POD test,
remain enabled. `Test::Pod` is declared so the POD test does not skip.

This macOS checkout lacks `Text::CSV`, so upstream tests were not claimed
locally. Exact-head target CI must establish the full test, build and installed
smoke result. A passing PR artifact would still not establish public RPM/SRPM
publication.
