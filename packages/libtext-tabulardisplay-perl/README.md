<!-- SPDX-License-Identifier: Apache-2.0 -->
# libtext-tabulardisplay-perl

The frozen inventory's exact `libtext-tabulardisplay-perl` key maps to Ubuntu
source 1.38-3 and the official [Text-TabularDisplay
1.38](https://metacpan.org/dist/Text-TabularDisplay) CPAN release. Ubuntu orig
tarball MD5 `f9d7dd9ed4ad8d34cdb0115aa12c79f5` matches the CPAN archive
byte for byte. Publisher `CHECKSUMS` and HTTPS archive both have SHA-256
`eb0990fafa56b667f23db764bdda5a4dc5f4b1ddc4b1383aa5eed6f22ed186e8`.
The archive has one root without traversal, links or special files. The
included COPYING is GPL version 2, and the module header explicitly grants
version 2 without an or-later option; the generic `open_source` metadata is
not used to broaden this to another license.

The official openEuler 24.03 LTS SP3 RVA23 `everything` primary metadata,
`primary.xml.zst` SHA-256
`fdb1663ee6c803e8efcc83c19b7a1548f047f08abba8a52f5fe623b222064d1a`,
contains neither `perl-Text-TabularDisplay` nor a
`perl(Text::TabularDisplay)` provider, and does contain the upstream test
dependency `perl(Test)`. This is a snapshot check, not a guarantee about
future repository contents.

`%check` retains all 17 default upstream `t/` files; 85 assertions passed on
local Perl 5.34.1. A source-level staging install yielded the module and man
page, both listed in the SPEC. Source examples that read `/etc/passwd` or
connect to MySQL are not installed as runnable helpers; none is a default
upstream test, and the library behavior is unchanged. Installed-RPM smoke
checks table rendering. Target CI must prove RPM build and installation.

Successful PR CI artifacts alone do not prove public RPM repository publication.
