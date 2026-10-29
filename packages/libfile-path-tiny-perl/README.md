<!-- SPDX-License-Identifier: Apache-2.0 -->
# libfile-path-tiny-perl

The frozen inventory's `libfile-path-tiny-perl` key records Ubuntu source
1.0-1. This package uses the official
[File-Path-Tiny 1.0](https://metacpan.org/dist/File-Path-Tiny) CPAN archive.
The HTTPS archive SHA-256
`2ec178da3b9899e4b466ab8b71edbb2bf23a0307ebe02fec7aa1f5826f61f55a`
matches the publisher's `CHECKSUMS` entry. Its single-root archive contains
only regular files and directories, with no traversal or links. The module
POD and README grant redistribution under Perl 5 terms, and no archive file
has a conflicting notice. The RPM uses the repository's Perl 5 dual-license
SPDX mapping, `GPL-1.0-or-later OR Artistic-1.0-Perl`.

The official openEuler 24.03 LTS SP3 RVA23 `everything` primary metadata,
SHA-256 `fdb1663ee6c803e8efcc83c19b7a1548f047f08abba8a52f5fe623b222064d1a`,
has neither `perl-File-Path-Tiny` nor `perl(File::Path::Tiny)`. It supplies
the core Carp, Cwd and File::Temp modules, `perl(Test::Exception)` 0.43,
and coreutils. This is a snapshot check, not a guarantee about future
repository contents.

The unchanged upstream default suite has nine files. Two functional files
exercise 52 assertions, including 22 deterministic symlink-toggle safety
checks using a temporary directory and `/bin/mkdir` and `/bin/mv`. The seven
other files are upstream author checks that explicitly skip unless
`RELEASE_TESTING` is set. The SPEC keeps all files and fails if either
required executable is missing, so the safety test cannot silently skip
for that reason. A clean local source run passed 52 assertions with the
seven author-only skips; a separate staged vendor install loaded the module
and exercised directory creation/removal. Exact-head target CI must still
prove RPM build, tests and installed smoke. PR artifacts are not public
publication.
