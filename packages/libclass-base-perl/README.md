<!-- SPDX-License-Identifier: Apache-2.0 -->
# Class::Base 0.09

The frozen Ubuntu `libclass-base-perl` 0.09-2 inventory key maps to official
stable [Class-Base 0.09](https://metacpan.org/dist/Class-Base). Publisher
CHECKSUMS and the independently downloaded 33,597-byte HTTPS archive agree on
SHA-256 `e1a5bdde52505802664a9108a515c9e8e502cb7229a49de94f4081b1b2aeed84`.
The archive has one top-level tree and only regular files/directories.

The installed `lib/Class/Base.pm`, bundled LICENSE, README and README.mkdn
grant redistribution under the same terms as Perl by copyright holder Andy
Wardley. The functional `t/test.t` repeats the grant; generated default test
files are covered by the distribution-wide LICENSE. CONTRIBUTORS lists helpers
but supplies no conflicting per-file notice, and no third-party code copy is
bundled. The RPM license expression records Perl's GPL version 1-or-later or
Artistic choice.

The official openEuler 24.03 LTS SP3 riscv64/RVA23 primary has no
`perl-Class-Base` package or `perl(Class::Base)` provider. It supplies the
runtime `Clone` provider and every build/test dependency, including CPAN::Meta
for the optional prereq-verification branch. The full three-file unchanged
upstream default suite passed locally with 47 assertions and zero skips.
Target CI must independently prove the same suite, physical RPM/SRPM products,
DNF installation and installed constructor/clone/error behavior. PR CI is not
repository publication.
