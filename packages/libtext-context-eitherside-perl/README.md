<!-- SPDX-License-Identifier: Apache-2.0 -->
# libtext-context-eitherside-perl

The frozen inventory's exact `libtext-context-eitherside-perl` key maps to
Ubuntu source 1.4-3, whose original tarball MD5
`5b4c816c9df69cd717393fbeab846ea1` matches the official
[Text-Context-EitherSide 1.4](https://metacpan.org/dist/Text-Context-EitherSide)
CPAN archive byte for byte. The publisher's `CHECKSUMS` entry and HTTPS
archive both have SHA-256
`bf0757d887243d3435ee8afaf796b16e54a2d9f44eafc69b0274c83ae57056e1`.
The archive has one root, with no traversal, links or special files. Although
legacy `META.yml` has an empty license field, README and module POD explicitly
grant Artistic-2.0 redistribution; `Changes` records the 1.4 relicensing.

The official openEuler 24.03 LTS SP3 RVA23 `everything` primary metadata,
`primary.xml.zst` SHA-256
`fdb1663ee6c803e8efcc83c19b7a1548f047f08abba8a52f5fe623b222064d1a`,
contains neither `perl-Text-Context-EitherSide` nor a
`perl(Text::Context::EitherSide)` provider. It has the declared build/test
dependencies, including Test::Pod and Test::Pod::Coverage. This is a snapshot
check, not a guarantee about future repository contents.

`%check` retains all three default upstream test files: functional, POD and
POD coverage. On local Perl 5.34.1, the functional and POD files passed
(11 assertions); POD coverage skipped because that local module is absent.
Target BuildRequires force that optional upstream suite to run in CI. A
source-level staging install yielded the module and man page, both listed in
the SPEC. Installed-RPM smoke checks version and extracted context.

Successful PR CI artifacts alone do not prove public RPM repository publication.
