<!-- SPDX-License-Identifier: Apache-2.0 -->
# libfile-copy-link-perl

The frozen inventory's exact `libfile-copy-link-perl` key maps to official
[File-Copy-Link 0.200](https://metacpan.org/dist/File-Copy-Link). The CPAN
HTTPS archive and `CHECKSUMS` entry both report SHA-256
`9cfa2f1b51b417126631b8ab24ee65d307fb8f76489acca6d66fada03ee59b29`.
All 32 archive entries remain under one top-level tree, without traversal
paths, links, or special files. The included `README` and both modules
expressly permit redistribution and modification under Perl's terms.

The official openEuler 24.03 LTS SP3 RVA23 `everything` primary metadata,
`primary.xml.zst` SHA-256
`fdb1663ee6c803e8efcc83c19b7a1548f047f08abba8a52f5fe623b222064d1a`,
has neither a `perl-File-Copy-Link` RPM nor `perl(File::Copy::Link)` or
`perl(File::Spec::Link)` providers. `perl-Test-Pod` 1.52 and
`perl-Test-Pod-Coverage` 1.10 are available. This snapshot check does not
guarantee future repository contents.

`%check` retains all nine default upstream test files, including the
symlink, command, POD and POD-coverage checks. Local Perl 5.34.1 passed
eight files and 52 assertions; `t/pod-coverage.t` skipped only because
`Test::Pod::Coverage` was not installed locally. The SPEC requires that
module on the target; target CI must prove the complete suite, and the
local skip is not counted as a full pass. The installed-RPM smoke uses a
temporary symlink to verify both packaged modules and the `copylink`
command without touching files outside its temporary directory.

Successful PR CI artifacts alone do not prove public RPM repository publication.
