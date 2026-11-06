# List::Keywords 0.11

Official source: `https://cpan.metacpan.org/authors/id/P/PE/PEVANS/List-Keywords-0.11.tar.gz`.
The publisher `CHECKSUMS` records SHA-256
`cab7922eae44b96fc2430aa10b2e726036605928d4e4fdf7e9c7b6ca32d4c64c`.
The archive has one safe root, only regular files/directories, and no patches.

The frozen Debian `0.11-2` and Ubuntu `0.11-2build4` lineage was marked
`license-blocked` because discovery metadata did not identify a license.
The official archive resolves that uncertainty: its `LICENSE` identifies Paul
Evans and grants redistribution under Perl's GPL-1.0-or-later or Artistic
terms, with matching grants in the module and XS sources. The distro rows are
lineage only, not licensing, dependency or target-build proof.

The official openEuler 24.03-LTS-SP3 riscv64 RVA23 primary lacks
`perl-List-Keywords` and `perl(List::Keywords)`. It uniquely provides
`perl(XS::Parse::Keyword::Builder) = 0.38` (upstream minimum 0.35),
`perl(XS::Parse::Keyword) = 0.38` (minimum 0.05), `perl(Module::Build) =
0.4234` (minimum 0.4004), and `perl(Test2::V0) = 0.000155` (minimum
0.000148), together with the compiler, Perl headers, CBuilder, Test::Pod,
List::Util, Time::HiRes, B::Deparse and Carp. Their target dependency closure
must be resolved by the package build.

All 13 default upstream test files are retained unchanged. The default POD
test condition is satisfied by a hard target `perl-Test-Pod` BuildRequires.
The benchmark-labelled file is retained; its single pass is not a performance
claim. The local macOS Perl has neither XS::Parse::Keyword::Builder nor a
new enough Test2::V0, so no local upstream build/test success is claimed.
Exact-head hosted target CI must prove all default tests without skips,
physical RPM/SRPM integrity, and installed functional smoke.
