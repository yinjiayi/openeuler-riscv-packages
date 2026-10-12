<!-- SPDX-License-Identifier: Apache-2.0 -->
# Data::Sorting 0.9

The frozen Ubuntu `libdata-sorting-perl` key maps to the official
[Data-Sorting 0.9](https://metacpan.org/dist/Data-Sorting) CPAN release. The
publisher's author-directory `CHECKSUMS` and an independent HTTPS download
agree on SHA-256 `055d83c70b200ce98e9177a7382f08afd72bf6f98c84ebca8570f1600288b386`.
The ordinary-file archive contains one source tree and no traversal paths.
The metadata's `unknown` license is an absence of a metadata declaration:
the release README and sole installed module POD explicitly permit use,
modification, and distribution under Perl's terms. Both Matthew Cavalletto
and Evolution Online Systems are credited for their respective portions,
with no conflicting grant in the bundled files.

The official openEuler 24.03 LTS SP3 riscv64/RVA23 primary has neither a
`perl-Data-Sorting` RPM nor a `perl(Data::Sorting)` provider. It uniquely
supplies Carp, Exporter, Test::More, and MakeMaker. All seven default
upstream `.t` files remain unchanged and load their bundled helper; local
`make test` passes 58 assertions without skips. Exact-head target CI must
prove the same suite, RPM build, installed functional smoke, and physical
products. PR CI artifacts do not establish public RPM publication.
