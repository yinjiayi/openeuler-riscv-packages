<!-- SPDX-License-Identifier: Apache-2.0 -->
# liblist-rotation-cycle-perl

The frozen inventory's exact `liblist-rotation-cycle-perl` key maps to
Ubuntu source 1.009-3 and the official stable CPAN List::Rotation::Cycle
1.009 release. Its HTTPS archive SHA-256
`103f9bb9e43b4c0396218b5c919258d28ef80b89074d96cd0d0240147b9f76f6`
matches publisher `CHECKSUMS`. All 20 archive entries are regular files or
directories under one root, with no traversal paths or links. The module
POD grants use under the same terms as Perl and META.yml says `perl`; this
resolves the frozen unknown-license marker for this exact release. The module
source is also installed as the license notice because the archive has no
standalone LICENSE file.

The official openEuler 24.03 LTS SP3 RVA23 `everything` primary metadata
(compressed SHA-256
`7023e5bb09a3a268acc6a411801bfabaf282d8569371f24cd63ede54f6c1dfbc`)
has no same-name RPM or `perl(List::Rotation::Cycle)` provider. It supplies
Perl, ExtUtils::MakeMaker, Test::Simple, Test::Pod, Test::Pod::Coverage,
perl-generators and make; Memoize is a Perl core module. This is a snapshot
check, not a guarantee about future repository contents.

All five unmodified default `t/*.t` files remain in `%check`; the POD modules
are BuildRequires so those tests execute. The upstream signature test
explicitly skips by default unless `TEST_SIGNATURE` is set; its skip must
not be counted as a verified cryptographic signature. Installed-RPM smoke
checks version, generated Provides, and a four-step wraparound sequence.
No local RPM/QEMU build was run. Target build, complete default tests and
installed smoke remain unverified until exact-head CI. PR artifacts are not
public repository publication.
