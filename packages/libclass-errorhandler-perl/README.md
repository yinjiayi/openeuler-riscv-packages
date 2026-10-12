<!-- SPDX-License-Identifier: Apache-2.0 -->
# Class::ErrorHandler 0.04

The frozen Ubuntu `libclass-errorhandler-perl` 0.04-3 inventory key maps to
official stable [Class-ErrorHandler 0.04](https://metacpan.org/dist/Class-ErrorHandler).
Publisher CHECKSUMS and the independently downloaded 9,821-byte HTTPS archive
agree on SHA-256
`342d2dcfc797a20bee8179b1b96b85c0ae7a5b48827359523cd8c74c3e704502`.
The archive has one top-level tree and only regular files/directories.

The installed `lib/Class/ErrorHandler.pm` and bundled README directly grant
same-as-Perl redistribution by original copyright holder Benjamin Trott;
bundled LICENSE declares the same terms for the distribution. Both default
tests are covered by that distribution grant; no third-party code is bundled.
The RPM license expression records Perl's GPL version 1-or-later or Artistic
choice.

The official openEuler 24.03 LTS SP3 riscv64/RVA23 primary has no
`perl-Class-ErrorHandler` package or `perl(Class::ErrorHandler)` provider. It
supplies EUMM, `Test` and `base` for the original tests; there is no non-core
runtime dependency. Both unchanged default `t/*.t` files passed locally with
10 assertions and zero skips. Target CI must independently prove the same
suite, physical RPM/SRPM products, DNF installation and both installed
class/object error branches. PR CI is not repository publication.
