<!-- SPDX-License-Identifier: Apache-2.0 -->
# libmath-basecalc-perl

The frozen discovery snapshot records Ubuntu source version 1.019-3 for
`libmath-basecalc-perl`. This package uses the official stable
[Math-BaseCalc 1.019](https://metacpan.org/dist/Math-BaseCalc) CPAN release.
The source SHA-256 is
`c74e2ba80ada8514b91134c7602e72b2cd330731c589597e951bf4a026efe9b8`,
matching publisher `K/KW/KWILLIAMS/CHECKSUMS` and an independent HTTPS
download. The archive has one root, 22 regular-file/directory entries and no
links, special files or traversal paths. It includes `SIGNATURE`, but no
publisher public key has been verified here; the fixed SHA-256 is the source
integrity gate.

The included `LICENSE` grants GPL version 1 or later or the Perl Artistic
License. The module POD and README repeat Perl 5 licensing, while Build.PL,
Makefile.PL and release metadata identify Perl licensing. No release file has
a conflicting per-file notice. The RPM license expression is
`GPL-1.0-or-later OR Artistic-1.0-Perl`.

Official openEuler 24.03 LTS SP3 RVA23 primary metadata (SHA-256
`fdb1663ee6c803e8efcc83c19b7a1548f047f08abba8a52f5fe623b222064d1a`)
has neither `perl-Math-BaseCalc` nor `perl(Math::BaseCalc)`. It has the
required `perl-Module-Build` 0.42.34, `perl-ExtUtils-MakeMaker` 7.70,
`perl-Test-Simple`, `perl-Math-BigInt`, `perl-Test-Pod-Coverage`, `perl-Carp`
and `perl-generators`. Upstream's configure/test requirements are kept, and
the available BigInt/POD test providers are explicit build requirements so
those tests can run rather than skip.

All eight original `t/*.t` files remain in `%check`. Six normal functional
files run by default. `t/99_podcoverage.t` requires both Test::Pod::Coverage
and `TEST_POD=1`; `%check` supplies both, adding coverage without modifying
the upstream test. `t/author-critic.t` explicitly skips unless
`AUTHOR_TESTING` is set; it is an author-only test, and target metadata has no
`perl-Test-Perl-Critic` provider. We preserve and report that skip rather than
pretend it passed. A clean local source-level test ran eight files and 78
assertions, with the POD coverage and author-only files explicitly skipped on
macOS because optional modules/author mode were absent. This local result is
not target RPM evidence.

The installed smoke checks the RPM/provider, module version and base-16/base-2
round trips. Target build, complete default test behavior and installed smoke
require exact-head hosted CI. PR artifacts do not prove public repository
publication.
