<!-- SPDX-License-Identifier: Apache-2.0 -->
# libtext-format-perl

The frozen inventory's exact `libtext-format-perl` key records Ubuntu source
0.63-1. Its original tarball MD5 `4c925a8f93c2a8209e9120a9198d769f`
matches the official CPAN [Text-Format
0.63](https://metacpan.org/dist/Text-Format) archive byte for byte. The
publisher's `CHECKSUMS` entry and HTTPS archive both have SHA-256
`fc64654f7d8da7071760ea0116e112b6d661b0a7bc3188dff1b2d52fb6a663cb`.
The archive stays beneath one root without traversal, links or special files.
LICENSE, Build.PL and module metadata grant the same GPL/Artistic terms as
Perl. This is `Text::Format`, distinct from `Text::FormatTable` and its
separate inventory key/package.

The official openEuler 24.03 LTS SP3 RVA23 `everything` primary snapshot,
`primary.xml.zst` SHA-256
`fdb1663ee6c803e8efcc83c19b7a1548f047f08abba8a52f5fe623b222064d1a`,
has neither `perl-Text-Format` nor a `perl(Text::Format)` provider and has
the upstream declared build and test dependencies. This snapshot check does
not guarantee future repository contents.

`%check` retains all three default upstream `t/` files: 15 assertions passed
with local Perl 5.34.1. Separate `xt/author` and `xt/release` checks are
upstream author/release suites, not default functional tests, and are not
claimed as passing. A source-level install produced the module and man page;
the SPEC lists both. Installed-RPM smoke checks deterministic word wrapping.
Exact target CI must prove RPM build and installation; PR artifacts alone do
not establish public RPM repository publication.
