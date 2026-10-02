<!-- SPDX-License-Identifier: Apache-2.0 -->
# libset-intspan-perl

This package maps the frozen Debian `libset-intspan-perl` 1.19-3,
Ubuntu `libset-intspan-perl` 1.19-3, Arch `perl-set-intspan` 1.19-9,
and Fedora `perl-Set-IntSpan` 1.19-37.fc44 lineages to Steven
McDougall's official SWMCD CPAN Set-IntSpan 1.19 archive. The
publisher `CHECKSUMS` and independent HTTPS download agree on SHA-256
`11b7549b13ec5d87cc695dd4c777cd02983dd5fe9866012877fb530f48b3dfd0`.
The archive has one safe top-level tree. Its sole installed module and
README explicitly grant redistribution under the same GPL/Artistic
terms as Perl, with no conflicting file-level notice. The grant-bearing
module is retained as the RPM license file. No upstream source or test
is changed.

Official openEuler 24.03 LTS SP3 RVA23 `repomd.xml` identifies primary
metadata SHA-256
`fdb1663ee6c803e8efcc83c19b7a1548f047f08abba8a52f5fe623b222064d1a`.
That verified primary metadata has neither a `perl-Set-IntSpan` RPM nor
a `perl(Set::IntSpan)` provider, and it does provide MakeMaker and Perl.
This target check is distinct from external distro lineage.

All 20 unchanged original default `t/*.t` files passed locally: 1,947
assertions, zero skips. `%check` runs that same default suite; only
exact-head target CI can establish the RVA23 result. Installed-RPM
smoke checks ownership, version, integer membership, union,
intersection, difference, and original-set immutability. PR CI products
do not establish public RPM publication.
