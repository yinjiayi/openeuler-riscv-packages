<!-- SPDX-License-Identifier: Apache-2.0 -->
# Class::Accessor::Children 0.02

The frozen Ubuntu `libclass-accessor-children-perl` 0.02-3 inventory key maps
to official stable [Class-Accessor-Children 0.02](https://metacpan.org/dist/Class-Accessor-Children).
Publisher CHECKSUMS and the independently downloaded 3,958-byte HTTPS archive
agree on SHA-256
`4b2e200849dec11f3fd368483d8d7de8db15096d7b91309994e016749a062928`.
The archive has one top-level tree and regular files/directories.

The frozen inventory's generic license-review hold is resolved for this fixed
archive by both installed `lib/Class/Accessor/Children.pm` and
`lib/Class/Accessor/Children/Fast.pm`: each directly names Yusuke Kawasaki and
grants redistribution under the same terms as Perl. README and META give the
same distribution-level choice; no third-party code copy is bundled. The RPM
license expression is Perl's GPL version 1-or-later or Artistic choice.

The official openEuler 24.03 LTS SP3 riscv64/RVA23 primary has no
`perl-Class-Accessor-Children` package or either module provider. It uniquely
supplies `Class::Accessor` and `Class::Accessor::Fast` 0.51, ExtUtils::MakeMaker,
Test::More, and Test::Pod 1.52. The latter is hard BuildRequired so the
upstream conditional POD test cannot silently skip.

All eight unchanged default `t/*.t` files passed locally with 112 assertions
and zero skips, including both normal and fast accessor paths. Target CI must
prove the same suite, physical RPM/SRPM products, DNF installation, and both
installed child-class branches. PR CI is not repository publication.
