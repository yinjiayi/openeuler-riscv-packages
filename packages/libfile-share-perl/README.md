<!-- SPDX-License-Identifier: Apache-2.0 -->
# libfile-share-perl

The frozen inventory's exact `libfile-share-perl` key maps to official
[File-Share 0.27](https://metacpan.org/dist/File-Share). The CPAN HTTPS
archive and its official `CHECKSUMS` entry both have SHA-256
`d6e8f4b55ebd38e0bb45e44392e3fa27dc1fde16abc5d1ff53e157e19a5755be`.
All archive paths stay under one top-level tree with no special file types.
The bundled `LICENSE` explicitly grants the GNU GPL version 1 or later
or the Perl Artistic License, resolving the frozen inventory's historical
`unverified-upstream` marker by direct release review.

The official openEuler 24.03 LTS SP3 RVA23 `everything` primary metadata,
`primary.xml.zst` SHA-256
`fdb1663ee6c803e8efcc83c19b7a1548f047f08abba8a52f5fe623b222064d1a`,
contains neither `perl-File-Share` nor a `perl(File::Share)` provider. It
contains `perl-Readonly` 2.05 and `perl-File-ShareDir` 1.118, meeting the
release's declared minimums. This snapshot check does not guarantee future
repository contents.

`%check` retains all three default upstream `t` files. Local Perl 5.34.1
with official Readonly 2.05 source in a temporary module path passed two
assertions; `t/author-pod-syntax.t` skipped by upstream's `AUTHOR_TESTING`
condition. The Readonly archive SHA-256
`4b23542491af010d44a5c7c861244738acc74ababae6b8838d354dfb19462b5e`
matched its CPAN `CHECKSUMS` entry. Separately, a private temporary library
and share directory demonstrated `dist_file` lookup. The installed-RPM smoke
repeats that functional check and verifies the RPM provider. Target QEMU
build and smoke remain unverified until exact-head CI; PR artifacts alone
do not establish public RPM repository publication.
