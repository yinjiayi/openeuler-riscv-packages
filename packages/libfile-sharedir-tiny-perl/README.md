<!-- SPDX-License-Identifier: Apache-2.0 -->
# libfile-sharedir-tiny-perl

The frozen inventory's exact `libfile-sharedir-tiny-perl` key maps to official
[File-ShareDir-Tiny 0.001](https://metacpan.org/dist/File-ShareDir-Tiny).
The CPAN `CHECKSUMS` entry and downloaded HTTPS archive both have SHA-256
`16d6e0352d02402cdd46bc8d7c426c66cd8488d7066878b250e50a6a34e47b58`.
All 23 archive entries are under one top-level tree, with no traversal paths,
links or special files. The complete `LICENSE` explicitly grants the Perl
GPL-1-or-later OR Artistic dual-license terms.

The official openEuler 24.03 LTS SP3 RVA23 `everything` primary metadata,
`primary.xml.zst` SHA-256
`fdb1663ee6c803e8efcc83c19b7a1548f047f08abba8a52f5fe623b222064d1a`,
contains neither `perl-File-ShareDir-Tiny` nor `perl(File::ShareDir::Tiny)`.
This is a snapshot check, not a guarantee about future state.

`%check` keeps all three default upstream test files: compile, functional
shared-directory resolution, and error cases. All 35 assertions passed on
local Perl 5.34.1. The `xt/author` POD checks are optional author tests,
not part of the default distribution test suite; they were not run.
Target CI must still prove the complete QEMU result. The installed-RPM
smoke creates a temporary shared-data tree and exercises all four public
lookup functions.

Successful PR CI artifacts alone do not prove public RPM repository publication.
