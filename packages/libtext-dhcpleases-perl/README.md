<!-- SPDX-License-Identifier: Apache-2.0 -->
# libtext-dhcpleases-perl

The frozen inventory's exact `libtext-dhcpleases-perl` key maps to Ubuntu
source version 1.0-3. This package uses the official stable
[Text-DHCPLeases 1.0](https://metacpan.org/dist/Text-DHCPLeases) CPAN
release. Its HTTPS tarball SHA-256
`677c68d5ede174202ea0aa5ea00256c5f5117f5028a18ddaad81640230ec53e8`
matches the publisher's `CHECKSUMS` entry. The single-root archive contains
only regular files and directories, with no traversal, links or special
files. The included README and module POD grant the same terms as Perl
itself despite the frozen metadata reporting an unknown license; the README
is installed as `%license` because no separate license text ships.

The official openEuler 24.03 LTS SP3 RVA23 `everything` primary metadata
(SHA-256 `fdb1663ee6c803e8efcc83c19b7a1548f047f08abba8a52f5fe623b222064d1a`)
contains neither `perl-Text-DHCPLeases` nor a
`perl(Text::DHCPLeases)` provider. It has Module::Build 0.4234 for the
upstream build system and Class::Struct 0.68 for the declared runtime
dependency. This is a snapshot check, not a guarantee about future
repository contents.

Both default upstream `t/*.t` files ran locally with the unmodified release:
32 assertions passed using the included DHCP lease fixture. A source-level
staging install yielded three modules and three manual pages, all listed in
the SPEC. Installed-RPM smoke checks the version, generated Provides and a
minimal lease parse/iterator count. Target RPM build, complete default suite
and installed smoke remain for CI to verify; successful PR artifacts alone
do not prove public repository publication.
