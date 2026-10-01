<!-- SPDX-License-Identifier: Apache-2.0 -->
# libtext-microtemplate-perl

The frozen inventory's exact `libtext-microtemplate-perl` key maps to
Ubuntu source 0.24-3 and official stable CPAN Text::MicroTemplate 0.24.
Its HTTPS archive SHA-256
`32801e71f35ee8aaa0d576cec125cee46b3d4915ae642bc64962120d4f97b4c8`
matches publisher `CHECKSUMS`. All 61 archive entries are regular files or
directories beneath one root; there are no traversal paths or links.
The main module POD grants the same terms as Perl itself, and both the
archived META and Makefile.PL declare `perl` licensing. This RPM uses the
repository's Perl 5 dual-license mapping
`GPL-1.0-or-later OR Artistic-1.0-Perl`; the main module is installed as
the license notice. The bundled `inc/Module::Install` is a build helper,
not a runtime file in the RPM.

The official openEuler 24.03 LTS SP3 RVA23 `everything` primary metadata
(compressed SHA-256
`7023e5bb09a3a268acc6a411801bfabaf282d8569371f24cd63ede54f6c1dfbc`)
has no same-name RPM or `perl(Text::MicroTemplate)` provider. It supplies
Perl, ExtUtils::MakeMaker, File::Temp, Test::Simple, IO::Scalar through
`perl-IO-stringy`, perl-generators and make. This is a snapshot check, not
a guarantee about future repository contents.

All 16 unmodified default `t/*.t` files remain in `%check`. Upstream
`t/05-warn.t` skips if IO::Scalar is missing; the SPEC requires its target
provider so that test will execute. The Perl 5.38 target also exceeds the
old-version conditional skip threshold in `t/07-file.t`. Installed-RPM
smoke checks version, generated Provides, basic rendering and HTML escaping.
No local RPM/QEMU build was run. Target build, complete tests and installed
smoke remain unverified until exact-head CI. PR artifacts are not public
repository publication.
