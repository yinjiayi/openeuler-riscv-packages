<!-- SPDX-License-Identifier: Apache-2.0 -->
# libset-scalar-perl

This package maps the frozen Debian `libset-scalar-perl` 1.29-3 and Fedora
`perl-Set-Scalar` 1.29-32.fc44 lineages to the official DAVIDO CPAN
Set-Scalar 1.29 archive. The CPAN publisher `CHECKSUMS` and independent
HTTPS download agree on SHA-256
`a3dc1526f3dde72d3c64ea00007b86ce608cdcd93567cf6e6e42dc10fdc4511d`.
The archive has one top-level tree with regular files only and no path
traversal. Its main module POD grants the entire library the same GPL or
Artistic terms as Perl; the seven related submodules and tests have no
conflicting author or license notice. The original grant-bearing module is
retained as the RPM license file. No upstream source or test file is patched.

The live openEuler 24.03 LTS SP3 RVA23 Everything `repomd.xml` identifies
primary metadata SHA-256
`fdb1663ee6c803e8efcc83c19b7a1548f047f08abba8a52f5fe623b222064d1a`.
That verified primary metadata has neither a `perl-Set-Scalar` RPM nor a
`perl(Set::Scalar)` provider and does supply the Perl/MakeMaker/Scalar::Util
capabilities used here. This target check is separate from external distro
lineage.

All 22 unchanged original `t/*.t` files passed locally: 2,652 assertions,
zero skips. `%check` runs the same default suite; only exact-head target CI
can confirm its RVA23 outcome. Installed-RPM smoke tests the module version,
RPM ownership, membership, union, intersection, difference, and source-set
immutability. PR CI products do not establish public RPM publication.
