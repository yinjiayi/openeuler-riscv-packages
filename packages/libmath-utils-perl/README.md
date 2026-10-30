<!-- SPDX-License-Identifier: Apache-2.0 -->
# libmath-utils-perl

The frozen discovery snapshot records Ubuntu source version 1.14-2 for
`libmath-utils-perl`. This package uses the official stable
[Math-Utils 1.14](https://metacpan.org/dist/Math-Utils) CPAN release. Its
source SHA-256 is
`88a20ae0736a622671b92bb2a350969af424d7610284530b277c8020235f2695`,
matching publisher `J/JG/JGAMBLE/CHECKSUMS` and an independent HTTPS download.
The archive has one root, 42 regular-file/directory entries, no links,
special files or traversal paths.

The included `LICENSE` expressly grants GPL version 1 or later or the Perl
Artistic License 1. The module POD and README grant the same Perl terms;
Build.PL and release metadata identify Perl licensing. Other release files
have no conflicting per-file notice. `Changes` notes a licensing wording
correction made in version 1.11; the current 1.14 archive's included grant
governs this source, rather than obsolete boilerplate. The RPM expression is
`GPL-1.0-or-later OR Artistic-1.0-Perl`.

Official openEuler 24.03 LTS SP3 RVA23 primary metadata (SHA-256
`fdb1663ee6c803e8efcc83c19b7a1548f047f08abba8a52f5fe623b222064d1a`)
has neither `perl-Math-Utils` nor `perl(Math::Utils)`. It has target Perl
5.38.0, upstream's `perl-Module-Build` configure requirement (target 0.42.34
versus minimum 0.4), `perl-Test-Simple`, `perl-Test-Pod` 1.52 (above the
POD test's 1.22 minimum), and `perl-generators`. The package explicitly
requires the available POD test provider so the default POD test runs.

All 22 unmodified upstream default `t/*.t` files remain in `%check`. The
`t/manifest.t` file intentionally skips unless `RELEASE_TESTING` is set; it
is a release-author check and target metadata does not provide its
`Test::CheckManifest` dependency. This skip is retained and reported, not
counted as a passing assertion. A clean local source-level run passed the
other 21 files, 138 assertions, including `t/pod.t`, on macOS Perl 5.34.1;
this is not target RPM evidence. Installed smoke checks the RPM/provider,
module version, GCD/LCM, sign and base-2 logarithm. Target build, default
tests and smoke require exact-head hosted CI. PR artifacts do not establish
public repository publication.
