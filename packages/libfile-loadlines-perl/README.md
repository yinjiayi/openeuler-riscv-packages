<!-- SPDX-License-Identifier: Apache-2.0 -->
# libfile-loadlines-perl

The frozen inventory's exact `libfile-loadlines-perl` key maps to official
[File-LoadLines 1.047](https://metacpan.org/dist/File-LoadLines). The CPAN
HTTPS archive and `CHECKSUMS` entry both report SHA-256
`26efd9682e4ecf91c1efe3e3e27bd8bcfaeea9c3c5e2eb432ed4f96968f84707`.
All 37 archive entries remain under one top-level tree, without traversal
paths, links, or special files. The included `README.md` and module POD
permit redistribution and modification under Perl's terms; `META.json` and
`Makefile.PL` likewise declare the Perl license.

The official openEuler 24.03 LTS SP3 RVA23 `everything` primary metadata,
`primary.xml.zst` SHA-256
`fdb1663ee6c803e8efcc83c19b7a1548f047f08abba8a52f5fe623b222064d1a`,
has neither a `perl-File-LoadLines` RPM nor a `perl(File::LoadLines)` provider.
Required target dependencies include `perl-Test-Exception` 0.43, `perl-URI`
5.10, and `perl-MIME-Base64` 3.16. This snapshot check does not guarantee
future repository contents.

`%check` retains all 14 default upstream test files and local fixture data;
all 284 assertions passed on local Perl 5.34.1. The default suite does not
fetch external data. The target CI must still prove the complete QEMU run.
The installed-RPM smoke loads CRLF text and verifies both decoded lines and
raw-blob content from a temporary file.

Successful PR CI artifacts alone do not prove public RPM repository publication.
