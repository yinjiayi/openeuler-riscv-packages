<!-- SPDX-License-Identifier: Apache-2.0 -->
# libtext-csv-unicode-perl

The frozen inventory's `libtext-csv-unicode-perl` key records Ubuntu source
0.400-2. This package uses the official [Text-CSV-Unicode 0.400](https://metacpan.org/dist/Text-CSV-Unicode)
CPAN release. The HTTPS archive SHA-256
`0187f439203c46bda5d916555b4381eaf86c35ce532691fa557a37182179f6d9`
matches the publisher's `CHECKSUMS`. The archive has one root, regular files
and directories only, and no traversal or links.

The current README and `lib/Text/CSV/Unicode.pm` grant the author's work
under Perl's terms. The module's inherited method documentation and
`t/base.t` derive from Alan Citterman's Text::CSV 0.01 (the latter's `test.pl`
is credited in the current README). The original official Text-CSV-0.01
archive, SHA-256
`5119f078b7cf863a94a9eff1ba4098cb3b93cd08895f872095f7ee3a07159bf9`,
explicitly grants the same Perl terms in both `README` and `CSV.pm`.
The original `test.pl` is part of that distribution grant. No shipped file
has a conflicting notice. The RPM uses the repository's Perl 5 dual-license
mapping, `GPL-1.0-or-later OR Artistic-1.0-Perl`.

The official openEuler 24.03 LTS SP3 RVA23 `everything` primary metadata,
SHA-256 `fdb1663ee6c803e8efcc83c19b7a1548f047f08abba8a52f5fe623b222064d1a`,
contains neither `perl-Text-CSV-Unicode` nor `perl(Text::CSV::Unicode)`.
It supplies `perl(Text::CSV)` 2.04, Module::Build, Test::Pod 1.52 and
Test::Pod::Coverage 1.10, so all five default test files can be required.
This is a repository snapshot, not a future-state guarantee.

The local macOS Perl lacks Text::CSV and Test::Pod::Coverage, so its full
upstream test suite is not claimed as passing. The SPEC retains all five
default test files and explicitly installs their dependencies; exact-head
target CI must establish their results and the installed smoke behavior.
PR artifacts alone do not prove public RPM repository publication.
