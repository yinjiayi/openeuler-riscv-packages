<!-- SPDX-License-Identifier: Apache-2.0 -->
# libtext-typography-perl

The frozen inventory's `libtext-typography-perl` key maps to Ubuntu and
Debian source version `0.01-5`. This package uses the official stable
[Text::Typography 0.01](https://metacpan.org/dist/Text-Typography) CPAN
release. Its HTTPS tarball SHA-256
`591e62d82507c77fe3be057a52f2a6da7fc2a38933c70204ef0f22dc0df91364`
matches the publisher's `CHECKSUMS` entry. The single-root archive contains
only regular files and directories, with no traversal or special files.

The automated CPAN metadata says `unknown` for license, but the only module's
POD contains John Gruber's complete three-clause BSD redistribution grant,
including the source/binary notice and non-endorsement conditions. The SPEC
uses `BSD-3-Clause` and installs that module as `%license` so the complete
notice accompanies the RPM. No separate license-text file is in the archive.

The official openEuler 24.03 LTS SP3 RVA23 `everything` primary metadata
(SHA-256 `fdb1663ee6c803e8efcc83c19b7a1548f047f08abba8a52f5fe623b222064d1a`)
contains neither `perl-Text-Typography` nor a `perl(Text::Typography)`
provider. It supplies `perl(Test::Pod)` 1.52 for the default POD test. This
is a snapshot check, not a guarantee about future repository contents.

Both default upstream `t/*.t` files passed their two assertions locally
without skips when `Test::Pod` was installed. Those tests cover loading and
POD syntax, not transformation semantics; installed-RPM smoke adds checks for
ellipsis and dash conversion and code-block preservation. A source-level
staging install yielded the module and manual page listed in `%files`.
Target RPM build, default tests, installed smoke and any public publication
remain for CI or later evidence to verify.
