<!-- SPDX-License-Identifier: Apache-2.0 -->
# libfile-fnmatch-perl

The frozen inventory's exact `libfile-fnmatch-perl` key maps to the latest
official [File-FnMatch 0.02](https://metacpan.org/dist/File-FnMatch).
The CPAN HTTPS archive and its official `CHECKSUMS` entry both have SHA-256
`962454b8e86bea8b132bf8af35757d0c6a8f5d599015bd6a5d68cb7ae7a9e916`.
All entries remain in one top-level tree without traversal paths, links,
or special files.

The frozen inventory marked this release `license-blocked`, while MetaCPAN
metadata reports an unknown license. Direct review of the release's README,
`FnMatch.pm` POD, and bundled `ppport.h` shows that all three expressly grant
redistribution and modification under Perl's terms. The SPEC records the
corresponding dual license; this is a source-level re-review, not a waiver
of the old inventory flag.

The official openEuler 24.03 LTS SP3 RVA23 `everything` primary metadata,
`primary.xml.zst` SHA-256
`fdb1663ee6c803e8efcc83c19b7a1548f047f08abba8a52f5fe623b222064d1a`,
contains neither `perl-File-FnMatch` nor a `perl(File::FnMatch)` provider.
It does provide the XS build dependencies and `perl(Test)`. This snapshot
check does not guarantee future repository contents.

`%check` retains both default upstream test files. Native macOS Perl 5.34.1
passed both files and 14 assertions; this is only a source-level portability
check, not an openEuler riscv64 build. The installed-RPM smoke checks the
native module and POSIX pathname matching. Exact-head target CI must prove
the riscv64 build, full tests, RPM contents and smoke. PR artifacts alone
do not establish public RPM repository publication.
