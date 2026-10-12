<!-- SPDX-License-Identifier: Apache-2.0 -->
# libmath-cartesian-product-perl

The frozen discovery snapshot records Ubuntu source version 1.009-4 for
`libmath-cartesian-product-perl`. This package uses the official stable
[Math-Cartesian-Product 1.009](https://metacpan.org/dist/Math-Cartesian-Product)
CPAN release. Its source SHA-256 is
`d0bf24e56aaebe47c9db6d09c257bc3bf5af2d0d69f060fe33c180a9c7199f32`,
matching publisher `P/PR/PRBRENAN/CHECKSUMS` and an independent HTTPS download.
The archive has one root, 13 regular-file/directory entries, no links,
special files or traversal paths.

The copyright holder's module POD and included `README` explicitly permit
use, redistribution and modification under the same terms as Perl 5. Both
Build.PL and META.json declare Perl licensing, and no release file has a
conflicting per-file grant. The archive does not contain a separate LICENSE
file; the README is installed with `%license` because it contains the express
grant. The RPM expression is `GPL-1.0-or-later OR Artistic-1.0-Perl`.

Official openEuler 24.03 LTS SP3 RVA23 primary metadata (SHA-256
`fdb1663ee6c803e8efcc83c19b7a1548f047f08abba8a52f5fe623b222064d1a`)
has neither `perl-Math-Cartesian-Product` nor
`perl(Math::Cartesian::Product)`. It has upstream's `perl-Module-Build`
configure requirement (target version 0.42.34 versus minimum 0.42),
`perl-Test-Simple` for Test::More, and `perl-generators`. This is a snapshot
of official target metadata, not a guarantee about future availability.

The complete unmodified upstream default test suite is `t/test.t`: 88
assertions, no skip branches. A clean local source-level `prove -Ilib t/test.t`
passed the one file and all 88 assertions on macOS Perl 5.34.1; this is not
target RPM evidence. `%check` retains the upstream `./Build test` action.
Installed smoke checks the RPM/provider, module version and a 2-by-2 Cartesian
product's contents. Target build, default tests and smoke require exact-head
hosted CI. PR artifacts do not establish public repository publication.
