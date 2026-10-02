<!-- SPDX-License-Identifier: Apache-2.0 -->
# libset-infinite-perl

This package maps the frozen Debian `libset-infinite-perl` 0.65-3,
Ubuntu `libset-infinite-perl` 0.65-3, Arch `perl-set-infinite` 0.65-7,
and Fedora `perl-Set-Infinite` 0.65-44.fc44 lineages to Flavio S.
Glock's official CPAN Set-Infinite 0.65 archive. The FGLOCK publisher
`CHECKSUMS` and an independent HTTPS download agree on SHA-256
`07bc880734492de40b4a3a8b5a331762f64e69b4629029fd9a9d357b25b87e1f`.
The archive contains a single safe top-level tree. All three installed
Perl modules identify the same author and grant redistribution on Perl's
GPL/Artistic terms; the included `LICENSE` spells out that choice. No
third-party code, contrary file-level license, patch, or modified test
was found.

The official openEuler 24.03 LTS SP3 RVA23 `repomd.xml` identifies
primary metadata SHA-256
`fdb1663ee6c803e8efcc83c19b7a1548f047f08abba8a52f5fe623b222064d1a`.
That verified primary metadata contains no `perl-Set-Infinite` package
or `perl(Set::Infinite*)` provider. It does provide the MakeMaker,
Test::More, and Time::Local capabilities required by the unchanged
distribution.

All 11 original default `t/*.t` files passed locally with 446
assertions and no skips. `%check` retains the complete default suite;
exact-head target CI must establish the RVA23 result. Installed-RPM
smoke checks module ownership, version, interval union, intersection,
and an open boundary. PR CI products do not establish public RPM
publication.
