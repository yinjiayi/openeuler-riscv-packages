<!-- SPDX-License-Identifier: Apache-2.0 -->
# Class::Factory::Util 1.7

The frozen Ubuntu `libclass-factory-util-perl` 1.7-5 inventory key maps to
official stable [Class-Factory-Util 1.7](https://metacpan.org/dist/Class-Factory-Util).
Publisher CHECKSUMS and the independently downloaded 11,942-byte HTTPS archive
agree on SHA-256
`6c516b445b44f87363fb3a148431d31e9ecb5e6f21fb6481c89b2406b6692e26`.
The archive contains one top-level tree and regular files/directories only.

The installed `lib/Class/Factory/Util.pm` and bundled README explicitly grant
same-as-Perl redistribution by Dave Rolsky; bundled LICENSE gives the full
Perl choice. This is also the original Alzabo copyright holder's grant:
[Alzabo 0.59](https://backpan.perl.org/authors/id/D/DR/DROLSKY/Alzabo-0.59.tar.gz)
(SHA-256 `a515146c5b11c762a0a8192579469b61064d0c5c29a2bec33c083ffaec710ecc`)
contains `lib/Alzabo/Util.pm` naming Dave Rolsky, and its LICENSE grants the
same terms. Official [Alzabo 0.92](https://cpan.metacpan.org/authors/id/D/DR/DROLSKY/Alzabo-0.92.tar.gz)
(publisher-matching SHA-256
`8a9373ef75e53052e11fa8c0ddd9b2839c298f6bf0c504e070208c48f201cfd4`)
records in Changes that Terrence Brannon separated this utility from Alzabo.
The four tiny `t/lib*` fixture classes are part of this source distribution,
with no contrary notice or third-party code copy. The RPM license expression
records Perl's GPL version 1-or-later or Artistic choice.

The official openEuler 24.03 LTS SP3 riscv64/RVA23 primary has no
`perl-Class-Factory-Util` package or module provider. It supplies Module::Build,
Test::Pod 1.52, Test::Pod::Coverage 1.10, Pod::Coverage 0.23, Test::More and
their provider dependencies. The three unchanged default tests locally ran
five functional assertions and one POD assertion, but the POD-coverage file
self-skipped because local Test::Pod::Coverage is absent. Target CI is required
to prove all three files and seven assertions without a skip, then physical
RPM/SRPM, DNF installation and installed subclass discovery. No local RPM or
QEMU build was run, and PR CI is not repository publication.
