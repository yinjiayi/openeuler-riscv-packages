<!-- SPDX-License-Identifier: Apache-2.0 -->
# libfile-copy-link-perl

The frozen inventory's exact `libfile-copy-link-perl` key maps to official
stable [File-Copy-Link 0.200](https://metacpan.org/dist/File-Copy-Link).
The official CPAN `CHECKSUMS` entry and downloaded HTTPS archive both have
SHA-256 `9cfa2f1b51b417126631b8ab24ee65d307fb8f76489acca6d66fada03ee59b29`.
Its 32 entries form one safe top-level tree without traversal paths, links or
special files. The bundled README, two modules and `copylink` script grant
Perl GPL/Artistic terms. This primary evidence resolves the frozen automated
`license-blocked` and `unverified-upstream` flags for this exact release.

The official openEuler 24.03 LTS SP3 RVA23 `everything` primary metadata,
`primary.xml.zst` SHA-256
`fdb1663ee6c803e8efcc83c19b7a1548f047f08abba8a52f5fe623b222064d1a`,
contains neither `perl-File-Copy-Link` nor the two Perl module Provides. This
is a snapshot check, not a guarantee about future repository state.

`%check` retains all nine default upstream test files. Test::Pod and
Test::Pod::Coverage are BuildRequires so their optional checks are actually
run. Symlink-dependent tests may self-skip if the target environment cannot
create symbolic links; exact counts must be taken from target CI. The installed
RPM smoke verifies both Perl module Provides and a `copylink` file-copy
roundtrip in an isolated temporary directory.

Successful PR CI artifacts alone do not prove public RPM repository publication.
