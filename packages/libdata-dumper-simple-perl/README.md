# Data::Dumper::Simple 0.11

Official source: `https://cpan.metacpan.org/authors/id/O/OV/OVID/Data-Dumper-Simple-0.11.tar.gz`.
Publisher `CHECKSUMS` records SHA-256
`3f3cfd278cbe118852d97a399de139a3dfce38c6e0f0c775a492d27e702f0c5e`,
matching the downloaded archive. The README and sole module explicitly grant
redistribution/modification under Perl terms by copyright holder Curtis Poe;
Build.PL declares `perl` licensing. Debian and Ubuntu `0.11-7` are frozen
lineage, not source or license authority.

The official openEuler 24.03-LTS-SP3 riscv64 RVA23 primary has neither
`perl-Data-Dumper-Simple` nor `perl(Data::Dumper::Simple)`. It uniquely
supplies `perl(Filter::Simple) = 0.94` (minimum 0.77), Data::Dumper,
Test::More, MakeMaker, `Test::Pod = 1.52` and
`Test::Pod::Coverage = 1.10`. Declared runtime dependencies are retained.

All six default upstream test files remain unchanged. Isolated local macOS
tests passed 36 assertions, but `t/pod-coverage.t` self-skipped because
Test::Pod::Coverage is absent locally. Hard target BuildRequires must enable
that file; exact-head hosted target CI must prove 6/6 without skips, source
filter behavior on target Perl, physical RPM/SRPM integrity and installed
functional smoke. The pure-Perl package is noarch without ELF debuginfo.
