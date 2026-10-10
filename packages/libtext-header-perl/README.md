<!-- SPDX-License-Identifier: Apache-2.0 -->
# libtext-header-perl

The frozen inventory's exact `libtext-header-perl` key records downstream
Ubuntu source version `1.03+pristine-2`; this package uses the official stable
CPAN Text::Header 1.03 archive, without the downstream `+pristine` suffix.
Its HTTPS archive SHA-256
`84cd282fd52066ed4240f41ba90e345e81670088667b46d40e58f000cd664856`
matches publisher `CHECKSUMS`. All seven archive entries are regular files or
directories under one root, without traversal paths or links.

The sole module's top copyright notice expressly permits GNU GPL version 2
or any later version. Its POD and the README also refer to a separate
Artistic License option without naming an Artistic version. This RPM selects
only the explicit `GPL-2.0-or-later` path; the original module is installed
as the license notice and the other source notices remain unmodified. This
resolves the frozen unknown-license marker for this exact release without
claiming an unproven Artistic SPDX version.

The official openEuler 24.03 LTS SP3 RVA23 `everything` primary metadata
(compressed SHA-256
`7023e5bb09a3a268acc6a411801bfabaf282d8569371f24cd63ede54f6c1dfbc`)
has no same-name RPM or `perl(Text::Header)` provider. Runtime modules are
Perl core only; make, Perl, ExtUtils::MakeMaker and perl-generators are
available for the target build. This is a snapshot check, not a future
repository guarantee.

The sole unmodified upstream default `test.pl` contains one load assertion
and remains in `%check`. Installed-RPM smoke adds version, generated Provides,
header formatting, and a simple parse round-trip; it does not prove security
handling of untrusted header contents. No local RPM/QEMU build was run.
Target build, default test and installed smoke remain unverified until
exact-head CI. PR artifacts are not public repository publication.
