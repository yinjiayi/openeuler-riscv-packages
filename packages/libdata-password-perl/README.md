<!-- SPDX-License-Identifier: Apache-2.0 -->
# Data::Password 1.12

The frozen Ubuntu `libdata-password-perl` key maps to the official
[Data-Password 1.12](https://metacpan.org/dist/Data-Password) CPAN release.
The publisher's author-directory `CHECKSUMS` and an independent HTTPS
download agree on SHA-256
`830cde81741ff384385412e16faba55745a54a7cc019dd23d7ed4f05d551a961`.
The ordinary-file archive has one source tree and no traversal paths. Though
CPAN metadata says `unknown`, the copyright holder Raz Information Systems
Ltd. explicitly grants same-Perl distribution terms in the release README
and sole installed module POD; no bundled file states conflicting terms.

The official openEuler 24.03 LTS SP3 riscv64/RVA23 primary has neither a
`perl-Data-Password` RPM nor a `perl(Data::Password)` provider. It uniquely
supplies Exporter, Test::More, MakeMaker, and Pod::Text. All three default
upstream `.t` files remain unchanged; local `make test` passes 34 assertions
without skips. The UNIX test has a conditional skip only if `getpwnam` is
unavailable; exact-head Linux target CI must prove it actually runs, plus
RPM build, installed functional smoke, and physical products. This package
implements legacy configurable checks and is not a modern password-strength
policy. PR CI artifacts do not establish public RPM publication.
