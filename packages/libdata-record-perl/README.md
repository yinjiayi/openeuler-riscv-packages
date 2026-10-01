# Data::Record 0.02

Official source: `https://cpan.metacpan.org/authors/id/O/OV/OVID/Data-Record-0.02.tar.gz`.
Publisher `CHECKSUMS` records SHA-256
`1d6ae66da2767520c21fbf12c538f1007ab27445d92c8eac763653f2b8849ebf`,
matching the downloaded archive. Its README and sole module explicitly grant
redistribution and modification under Perl terms by copyright holder Curtis
Poe; Build.PL declares `perl` licensing. Debian and Ubuntu `0.02-8` are frozen
lineage, not source or license authority.

The official openEuler 24.03-LTS-SP3 riscv64 RVA23 primary lacks both
`perl-Data-Record` and `perl(Data::Record)`. It uniquely supplies declared
`perl(Sub::Uplevel) = 0.2800` (minimum 0.09), `perl(Test::Exception) = 0.43`
(minimum 0.21), MakeMaker, Test::More, `Test::Pod = 1.52`,
`Test::Pod::Coverage = 1.10`, Carp and Data::Dumper. The upstream-declared
Sub::Uplevel runtime dependency is retained even though the module does not
currently load it directly; the full target closure must resolve with DNF.

All four default upstream test files remain unchanged. The isolated local
macOS run passed 31 assertions, but `t/pod-coverage.t` self-skipped because
Test::Pod::Coverage is not installed locally. Hard target BuildRequires must
enable that test; exact-head hosted target CI must prove 4/4 files with no
skips, physical RPM/SRPM integrity, and installed functional smoke. This
pure-Perl package is noarch and produces no ELF debuginfo.
