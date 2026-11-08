<!-- SPDX-License-Identifier: Apache-2.0 -->
# libmime-encwords-perl

This package maps Ubuntu's `libmime-encwords-perl` source to the official CPAN
MIME::EncWords 1.015.0 release. Its 38,971-byte archive has SHA-256
`23ef065897821337bdd16487e65e2a3798383348225c72cd762bb3741ad009b5`,
matching the publisher's `CHECKSUMS`. The archive has 41 entries beneath one
root, without links or traversal entries.

The archived README and both module copyright notices explicitly grant the
same terms as Perl itself. Archived `GPL` and `ARTISTIC` files carry the
license texts. The RPM maps the author grant to
`GPL-1.0-or-later OR Artistic-1.0-Perl`; the `META.json` license field is
`unknown`, so the archived grant is the operative evidence.

The official openEuler 24.03 LTS SP3 RVA23 primary metadata (compressed SHA-256
`fdb1663ee6c803e8efcc83c19b7a1548f047f08abba8a52f5fe623b222064d1a`)
contains neither `perl-MIME-EncWords` nor `perl(MIME::EncWords)`. It provides
the required `perl(MIME::Charset)` 1.013.1, `perl(MIME::Base64)` 3.16 and
`perl(Encode)` 3.21, as well as `perl(Test::Pod)` 1.52. This is a repository
snapshot, not a promise about future contents.

`%check` retains all six unmodified upstream `t/*.t` files. The Test::Pod
build requirement ensures the optional POD test can run on target; older
Perl/EBCDIC skip branches should not apply on this target, but exact counts
and skips need CI confirmation. Installed-RPM smoke checks both module
providers and a UTF-8 MIME header decode. A local Perl-only install probe
identified the files; no local RPM or QEMU build was run. Target behavior and
physical RPM/SRPM bytes require exact-head hosted PR CI. CI artifacts are not
repository publication.
