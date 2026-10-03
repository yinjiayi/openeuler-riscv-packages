# Date::HolidayParser 0.43

The frozen 2026-08-08 inventory includes Fedora Everything-source
`perl-Date-HolidayParser` 0.43-16.fc44. This package uses the official
ZERODOGG CPAN 0.43 tarball with SHA-256
`d61f6850e669e41d221e598fd09d9ec2f29a8138d9679609f02a31bb817e0a6b`,
matching the publisher's `CHECKSUMS` entry. The official openEuler
24.03-LTS-SP3 riscv64 RVA23 primary metadata contains neither the same RPM nor
`perl(Date::HolidayParser)` / `perl(Date::HolidayParser::iCalendar)` and does
contain the required `perl(Moo)` 2.005005 provider and default-test providers.

The archive's top-level `COPYING` grants the program under GPL-3.0-or-later
or the bundled Artistic license. The two installed modules name Eskild
Hustvedt and grant same-as-Perl terms, making Artistic-1.0 a common explicit
option. The package declares only that common option, not a broader GPL-only
reading. Fedora's metadata records the two notice families conjunctively;
the archive text, not that summary, is the redistribution basis. No contrary
file-level grant was found among the two modules, tests, fixture, build
metadata and documentation.

The original three default test files and 374 assertions are unchanged. The
third file exercises GMT, CET and EST; `%check` sets `TZ=GMT` to avoid adding
an unrelated inherited fourth zone, and requires all three files, all 374
assertions and no skip. The installed smoke test reads a holiday definition
through the base parser and its iCalendar companion. This PR verifies only
GitHub-hosted pull-request builds; it does not merge or publish the package.
