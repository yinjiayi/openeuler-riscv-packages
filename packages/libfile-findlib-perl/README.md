<!-- SPDX-License-Identifier: Apache-2.0 -->
# libfile-findlib-perl

The frozen inventory's exact `libfile-findlib-perl` key maps to official
[File-FindLib 0.001004](https://metacpan.org/dist/File-FindLib). The
CPAN `CHECKSUMS` entry and downloaded HTTPS archive both have SHA-256
`c047e5bfac1bb05ff31b207f2b2510fcaca4f11e134a915db046248b01f4e5e5`.
All 24 archive entries are under one top-level tree; there are no traversal
paths, links or special files. The release's `LICENSE` contains the full
Unlicense public-domain dedication.

The official openEuler 24.03 LTS SP3 RVA23 `everything` primary metadata,
`primary.xml.zst` SHA-256
`fdb1663ee6c803e8efcc83c19b7a1548f047f08abba8a52f5fe623b222064d1a`,
contains neither `perl-File-FindLib` nor `perl(File::FindLib)`. It includes
the Perl build and test dependencies. This is a snapshot check, not a
guarantee about future state.

`%check` retains all three default upstream tests: basic loading, lookup
including a symbolic-link fixture, and `%INC` update. All 20 assertions
passed on local Perl 5.34.1 in a fresh source tree. The target CI must
still prove the complete QEMU run. The installed-RPM smoke creates a
temporary nested tree and verifies ancestor library resolution and module
loading.

Successful PR CI artifacts alone do not prove public RPM repository publication.
