<!-- SPDX-License-Identifier: Apache-2.0 -->
# Class::Adapter 1.09

The frozen `libclass-adapter-perl` inventory key and Debian source package
`libclass-adapter-perl` 1.09-2 map to official stable
[Class-Adapter 1.09](https://metacpan.org/dist/Class-Adapter). Publisher
CHECKSUMS and the independently downloaded 33,256-byte HTTPS archive agree
on SHA-256
`5a19e99da44a9d6e1dc7160e23cfe912d42fb49386d6b5af6184c4ac0741bb27`.
The archive has one top-level tree, regular files and no vendored code.

Each of the three installed modules, `Class/Adapter.pm`,
`Class/Adapter/Builder.pm` and `Class/Adapter/Clear.pm`, directly grants
same-as-Perl redistribution by Adam Kennedy in its POD. Bundled README and
LICENSE agree, and the eight default test files have no contrary notice.
The RPM license expression records Perl's GPL version 1-or-later or Artistic
choice. Upstream `xt/` author/release tests are not in the default `t/*.t`
suite. The original archive marks modules owner-only executable, but a local
EUMM staged install produced readable module files and all three man pages.

The official openEuler 24.03 LTS SP3 riscv64/RVA23 primary has no
`perl-Class-Adapter` package or module provider. It supplies Scalar::Util
1.63, Carp, base, constant, CPAN::Meta, EUMM, File::Spec and Test::More.
All eight unchanged default files locally passed 65 assertions without a
skip. Target CI must prove the same suite, physical RPM/SRPM, DNF install
and installed object delegation. No local RPM or QEMU build was run, and PR
CI is not repository publication.
