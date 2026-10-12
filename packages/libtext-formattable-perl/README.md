<!-- SPDX-License-Identifier: Apache-2.0 -->
# libtext-formattable-perl

The frozen inventory's exact `libtext-formattable-perl` key records Ubuntu
source 1.03-3. Its upstream original tarball has MD5
`f97ad335d77095c296f8c672fee08f5b`, exactly matching the official CPAN
[Text-FormatTable 1.03](https://metacpan.org/dist/Text-FormatTable) release.
That byte-level match establishes the inventory-to-upstream name mapping.
The official CPAN HTTPS archive and publisher `CHECKSUMS` both record SHA-256
`587e94aaef1a80dab520770e18075a41b7e59add95bf6dd817bd4059b902799f`.
Its archive has one top-level root and no traversal, links or special files.
Makefile.PL, README and module POD grant the same license terms as Perl.
Upstream declares no source-repository URL, so the metadata links to its
canonical CPAN page rather than inventing a VCS location.

The official openEuler 24.03 LTS SP3 RVA23 `everything` primary snapshot,
`primary.xml.zst` SHA-256
`fdb1663ee6c803e8efcc83c19b7a1548f047f08abba8a52f5fe623b222064d1a`,
has neither `perl-Text-FormatTable` nor a `perl(Text::FormatTable)` provider.
It does provide the upstream test and build dependencies. This snapshot
check does not guarantee future repository contents.

`%check` runs upstream's complete default `test.pl`: all five assertions
passed with local Perl 5.34.1. The upstream MakeMaker install also copies
`example.pl` into the generic vendorlib `Text/` namespace. The SPEC removes
that incidental module-path copy from the buildroot but retains the same
example as `%doc`; the functional module and man page remain installed.
Installed-RPM smoke checks rendering. Exact target CI must prove the RPM
build and installation; a PR artifact alone is not public RPM publication.
