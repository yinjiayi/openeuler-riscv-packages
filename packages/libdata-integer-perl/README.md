# Data::Integer 0.007

Official source: `https://cpan.metacpan.org/authors/id/R/RR/RRWO/Data-Integer-0.007.tar.gz`.
Publisher `CHECKSUMS` records SHA-256
`cd635ecc814122f12e3103daab0c0a9323070a1316a5f4152c3e26ae7745473d`,
matching the downloaded archive. Its sole module and README explicitly grant
redistribution and modification under Perl terms by copyright holder Andrew
Main; Makefile.PL declares `perl` licensing. Debian and Ubuntu `0.007-1` are
frozen lineage, not source or license authority.

The official openEuler 24.03-LTS-SP3 riscv64 RVA23 primary lacks both
`perl-Data-Integer` and `perl(Data::Integer)`. It uniquely supplies Perl's
Carp, Exporter, constant, integer and parent providers, MakeMaker,
Test::More, `Test::Pod = 1.52` and `Test::Pod::Coverage = 1.10`.
The two POD providers are hard BuildRequires to run the complete default
suite, not optional skips.

All ten default upstream test files remain unchanged. The isolated local
macOS Perl run passed 6,270 assertions, but `t/pod_cvg.t` self-skipped because
Test::Pod::Coverage is not installed locally. That local result is partial:
exact-head hosted target CI must prove 10/10 files with no skips, physical
RPM/SRPM integrity, and installed functional smoke. This pure-Perl source
contains no ELF payload, so its SPEC marks the package noarch and suppresses
empty debuginfo generation.
