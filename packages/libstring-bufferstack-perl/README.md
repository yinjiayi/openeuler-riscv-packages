<!-- SPDX-License-Identifier: Apache-2.0 -->
# libstring-bufferstack-perl

The frozen inventory's exact `libstring-bufferstack-perl` key maps to the
official stable CPAN String::BufferStack 1.16 release. Its HTTPS archive
SHA-256 `812181c2e73ebb71b3c687bbb7aed97bb8b66df2a64d18bd8843dc0c4b083392`
matches publisher `CHECKSUMS`. All 27 entries are regular files or
directories beneath one root, with no links or traversal paths. The
vendored `inc/Module::Install` files are build helpers, not RPM runtime files.

The module POD and README expressly say the package is distributed under
the same terms as Perl itself, and archived META declares `license: perl`.
This RPM uses the repository's Perl 5 dual-license mapping
`GPL-1.0-or-later OR Artistic-1.0-Perl` and installs the module POD as its
license notice. These release-specific facts resolve the frozen index's
historical `license-blocked` and `unverified-upstream` discovery decisions.

The official openEuler 24.03 LTS SP3 RVA23 `everything` primary metadata
(compressed SHA-256
`fdb1663ee6c803e8efcc83c19b7a1548f047f08abba8a52f5fe623b222064d1a`)
has no same-name RPM or `perl(String::BufferStack)` provider. It supplies
Perl, ExtUtils::MakeMaker, Test::More via perl-Test-Simple, perl-generators,
make and findutils. This is a snapshot check, not a guarantee about future
repository contents.

All five unmodified default upstream test files (169 declared assertions)
remain in `%check`. The only conditional skip is for a Perl 5.6 limitation;
the target Perl exceeds that threshold. Installed-RPM smoke checks version,
generated Provides, nested buffering, filter behavior and output flush.
No local RPM/QEMU build was run. Target build, complete tests and installed
smoke remain unverified until exact-head CI. PR artifacts are not public
repository publication.
