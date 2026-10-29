# Data::Buffer 0.06

Official source: `https://cpan.metacpan.org/authors/id/T/TI/TIMLEGGE/Data-Buffer-0.06.tar.gz`.
Publisher `CHECKSUMS` records SHA-256
`815956260f846095f12e1682da6f6d6857a2512dcf394dbc569293102b8fe4ad`,
matching the downloaded archive. Bundled LICENSE and the sole module
explicitly grant redistribution/modification under Perl's GPL-1.0-or-later
or Artistic terms by copyright holder Benjamin Trott; no conflicting
per-file grant appears. Debian `0.06-1` is frozen lineage only.

The official openEuler 24.03-LTS-SP3 riscv64 RVA23 primary has neither
`perl-Data-Buffer` nor `perl(Data::Buffer)`. It uniquely supplies MakeMaker
and `perl(Test2::V0) = 0.000155`, the source's sole external test dependency.
The full target dependency transaction remains a CI gate.

The sole default upstream test file is unmodified and plans 55 assertions.
It passed locally on macOS (`Files=1, Tests=55`, no skips), but this is not
target build evidence. Exact-head hosted target CI must prove all 55 under
the locked SP3 RVA23 image, physical RPM/SRPM integrity and installed
functional smoke. This pure-Perl payload is noarch and has no ELF debuginfo.
