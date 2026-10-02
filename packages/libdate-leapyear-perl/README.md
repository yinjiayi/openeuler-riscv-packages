<!-- SPDX-License-Identifier: Apache-2.0 -->
# Date::Leapyear 1.72

The frozen `libdate-leapyear-perl` inventory key and official Debian source
package `libdate-leapyear-perl` 1.72-3 map to the stable CPAN
[Date-Leapyear 1.72](https://metacpan.org/dist/Date-Leapyear). The RBOW
publisher CHECKSUMS and independently downloaded 11,153-byte HTTPS archive
agree on SHA-256
`706360e57a85cf5c0de1cc6502d0366e876df7b42a2e60192861a273750fa603`.

The official archive's top-level `LICENSE` expressly says that this module is
licensed on the same terms as Perl, naming GPL version 1-or-later or the
Artistic License. The only installed code file, `lib/Date/Leapyear.pm`, names
Rich Bowen as author. Its three test files and build files contain no contrary
notice, and there is no vendored code. Upstream `META.yml` and MetaCPAN mark
the license `unknown`; that incomplete metadata is not treated as the grant.
The explicit distribution license covers this one-module archive, and the RPM
license expression records its GPL-or-Artistic choice. If an unobserved rights
holder or conflicting per-file grant emerges, this conclusion must be revisited.

The official openEuler 24.03 LTS SP3 riscv64/RVA23 primary has no
`perl-Date-Leapyear` package or `perl(Date::Leapyear)` provider. It supplies
Exporter 5.77, ExtUtils::MakeMaker 7.70, Test::More 1.302198, and Perl 5.38
strict/vars. All three unchanged default files locally passed 764 assertions
from fixed leap-year tables without a skip. Target CI must prove the same
suite, physical RPM/SRPM, DNF installation and installed boundary-year
checks. No local RPM or QEMU build was run, and PR CI is not publication.
