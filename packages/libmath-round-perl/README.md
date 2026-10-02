<!-- SPDX-License-Identifier: Apache-2.0 -->
# libmath-round-perl

The frozen discovery snapshot's exact `libmath-round-perl` row records Ubuntu
source version 0.08-1. This package uses the official stable
[Math-Round 0.08](https://metacpan.org/dist/Math-Round) CPAN archive. Its
SHA-256 is `7b4d2775ad3b859a5fd61f7f3fc5cfba42b1a10df086d2ed15a0ae712c8fd402`,
matching publisher `N/NE/NEILB/CHECKSUMS` and an independent HTTPS download.
The archive has one root, 14 regular-file/directory entries, and no links,
special files or traversal paths.

The copyright holder's included `LICENSE` grants the same terms as Perl 5:
GPL version 1 or any later version, or Artistic License 1. The installed
`lib/Math/Round.pm` POD and README repeat that grant. The remaining release
files have no conflicting per-file notice; META and `dist.ini` also specify
Perl 5 terms. The RPM license expression is
`GPL-1.0-or-later OR Artistic-1.0-Perl`.

The official openEuler 24.03 LTS SP3 RVA23 `everything` primary metadata
(SHA-256 `fdb1663ee6c803e8efcc83c19b7a1548f047f08abba8a52f5fe623b222064d1a`)
contains neither `perl-Math-Round` nor `perl(Math::Round)`. It does contain
`perl`, `perl-Exporter`, `perl-parent`, `perl-ExtUtils-MakeMaker`,
`perl-Test-Simple`/`perl(Test::More)` and `perl-generators`; the other declared
runtime modules are provided by the target Perl core packages. This is a
repository snapshot check, not a guarantee about future contents.

The unmodified upstream default `t/02-original.t` contains ten top-level
assertions and no skip branches. A clean local source-level `make test` ran
that one file and passed all ten assertions on macOS Perl 5.34.1; this is not
target RPM evidence. A staged source-level `pure_install` produced the module
and `Math::Round` manual page listed by the SPEC. `%check` retains the complete
`make test`.
The installed-RPM smoke verifies the package, generated module provider,
version, ordinary rounding, even-tie rounding and nearest-multiple behavior.
Target build, `%check` and installed smoke require exact-head CI; successful PR
artifacts do not by themselves prove public repository publication.
