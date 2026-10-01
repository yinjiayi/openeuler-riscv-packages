<!-- SPDX-License-Identifier: Apache-2.0 -->
# libstring-mkpasswd-perl

The frozen inventory's exact `libstring-mkpasswd-perl` key maps to Ubuntu
source 0.05-3 and the official stable CPAN String::MkPasswd 0.05 release.
Its HTTPS archive SHA-256
`5310f83460045475071666b5423db2f0aa82d6685c802ec7abe6c2c410639b96`
matches the publisher's `CHECKSUMS` entry. The archive contains one root and
only regular files and directories, without traversal paths or links.
The included LICENSE grants redistribution under GPL-1-or-later or
Artistic-1.0-Perl, resolving the frozen unknown-license metadata for this
exact release.

The official openEuler 24.03 LTS SP3 RVA23 `everything` primary metadata
(compressed SHA-256
`7023e5bb09a3a268acc6a411801bfabaf282d8569371f24cd63ede54f6c1dfbc`)
has no same-name RPM or `perl(String::MkPasswd)` provider. It supplies Perl,
ExtUtils::MakeMaker, Test::Simple, perl-generators and make. This is a
snapshot check, not a guarantee about future repository contents.

All five unmodified upstream default test files remain in `%check`; the
fifth contains two nested sets of 100 no-ambiguous-character assertions.
The installed-RPM smoke verifies the generated Perl provider, module
version, command syntax, character-class output, and invalid-request
behavior. The generator uses Perl's `rand` and is not a cryptographic
secret generator; packaging it is not an entropy or security assurance.
No local RPM/QEMU build was run. Target build, complete tests and installed
smoke remain unverified until exact-head CI. PR artifacts are not public
repository publication.
