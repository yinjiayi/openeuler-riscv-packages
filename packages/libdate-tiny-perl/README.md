<!-- SPDX-License-Identifier: Apache-2.0 -->
# Date::Tiny 1.07

The frozen `libdate-tiny-perl` inventory key and official Debian source
package `libdate-tiny-perl` 1.07-2 map to stable CPAN
[Date-Tiny 1.07](https://metacpan.org/dist/Date-Tiny). Publisher CHECKSUMS
and the independently downloaded 20,776-byte HTTPS archive agree on SHA-256
`6d7539e0be273d789575544f00c8ba1aa857d22f41d2cb3f40fa8681dc6f3b8e`.

The only installed module `lib/Date/Tiny.pm` directly grants same-as-Perl
redistribution, crediting Adam Kennedy and describing David Golden as its
caretaker. The top-level LICENSE says this software is redistributable on
those terms; README and both META files agree. The two default test files,
generated prerequisite data and build metadata have no contrary notice or
vendored code. The RPM license expression records the GPL version
1-or-later or Artistic choice for this distribution-wide grant.

Official openEuler 24.03 LTS SP3 riscv64/RVA23 primary has no
`perl-Date-Tiny` package or `perl(Date::Tiny)` provider. It supplies Carp,
overload, ExtUtils::MakeMaker, File::Spec, Test::More, CPAN::Meta and
DateTime 1.58 with Locale 1.35 and TimeZone 2.62. DateTime is a hard build
dependency to exercise the upstream optional conversion branch, but remains
optional at runtime as upstream declares it.

The unmodified default suite has two files/20 assertions. It passes locally
with DateTime::Locale 1.25, but against independently executed official 1.35
it fails only original `t/02_main.t` assertion 10: the constructor returns
`en-US` for `C`, whereas the test's old version heuristic expects
`en-US-POSIX`. The package-local patch preserves that assertion and all 20
tests, comparing with explicit constants for 1.35+, 1.00–1.34 and older.
Both 1.25 and 1.35 branches passed the complete patched 2-file suite with
zero skips. Target CI must still prove the full suite, physical RPM/SRPM,
DNF installation and installed date-object roundtrip. No local RPM or QEMU
build was run, and PR CI is not publication.
