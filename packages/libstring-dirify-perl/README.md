<!-- SPDX-License-Identifier: Apache-2.0 -->
# libstring-dirify-perl

The frozen inventory's exact `libstring-dirify-perl` key maps to Ubuntu and
official CPAN version 1.03. The HTTPS release tarball SHA-256
`8e66374ade8b447ba94d276616973ef8a249e5b6258b81662142daa712329d53`
matches publisher `CHECKSUMS`. The archive has one root and only regular
files and directories, with no traversal, links or special files. The
included `LICENSE` expressly grants the same terms as Perl itself (GPL 1
or later OR Artistic); `META.json` declares `perl_5`. The RPM uses
`GPL-1.0-or-later OR Artistic-1.0-Perl` and installs the license text.

The official openEuler 24.03 LTS SP3 RVA23 `everything` primary metadata
(SHA-256 `fdb1663ee6c803e8efcc83c19b7a1548f047f08abba8a52f5fe623b222064d1a`)
has neither `perl-String-Dirify` nor a `perl(String::Dirify)` provider.
The declared `perl(Test::Pod)` dependency is present at version 1.52.
Runtime dependencies are Perl core modules only. This snapshot check does
not guarantee future repository contents.

All three unmodified default upstream `t/*.t` files ran locally: 13 tests
passed without skips. The separate `xt/author/pod.t` is an author-only
test, not part of the default `make test`, and is not counted as passed.
The installed-RPM smoke checks the module version, default/custom separator
and HTML conversion. Target RPM build, full default suite and installed
smoke remain for CI; successful PR artifacts alone do not prove public
publication.
