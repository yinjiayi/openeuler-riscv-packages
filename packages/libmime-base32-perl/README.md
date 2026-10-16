<!-- SPDX-License-Identifier: Apache-2.0 -->
# libmime-base32-perl

This package maps Ubuntu's `libmime-base32-perl` source to the official
MIME::Base32 1.303 CPAN release. Its 14,121-byte source archive has SHA-256
`ab21fa99130e33a0aff6cdb596f647e5e565d207d634ba2ef06bdbef50424e99`,
matching the publisher's `CHECKSUMS` file. The archive has 18 regular files
and directories beneath one root, with no links or traversal entries.

The archived `LICENSE` explicitly permits GPL version 1 or later or the
Artistic License and ships both license texts. `META.json` calls this
`perl_5`. The RPM records the explicit grant as
`GPL-1.0-or-later OR Artistic-1.0-Perl` and installs the notices.

The official openEuler 24.03 LTS SP3 RVA23 primary metadata (compressed
SHA-256 `fdb1663ee6c803e8efcc83c19b7a1548f047f08abba8a52f5fe623b222064d1a`)
contains neither `perl-MIME-Base32` nor `perl(MIME::Base32)`; it has the
Perl and test/build providers. The scan is a repository snapshot, not a
promise about future contents.

`%check` runs upstream's default `make test`: both unmodified `t/*.t`
files. `Makefile.PL` also names `xt/*.t`, but this archive has no `xt`
tests. Installed-RPM smoke exercises the RPM provider and Base32/base32hex
round trips. No local RPM or QEMU build was run; target results require
exact-head PR CI. CI artifacts are not repository publication.
