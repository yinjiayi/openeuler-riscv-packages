<!-- SPDX-License-Identifier: Apache-2.0 -->
# libfile-grep-perl

The frozen inventory's exact `libfile-grep-perl` key maps to official
[File-Grep 0.02](https://metacpan.org/dist/File-Grep). The CPAN `CHECKSUMS`
entry and downloaded HTTPS archive both have SHA-256
`462e15274eb6278521407ea302d9eea7252cd44cab2382871f7de833d5f85632`.
All 11 archive entries are under one top-level tree, with no traversal paths,
links or special files. The README explicitly grants redistribution and
modification under Perl's terms and references the Artistic License; the
RPM uses the repository's standard Perl dual-license expression.

The official openEuler 24.03 LTS SP3 RVA23 `everything` primary metadata,
`primary.xml.zst` SHA-256
`fdb1663ee6c803e8efcc83c19b7a1548f047f08abba8a52f5fe623b222064d1a`,
contains neither `perl-File-Grep` nor `perl(File::Grep)`. This is a snapshot
check, not a guarantee about future state.

`%check` retains the sole default upstream test file and all 11 assertions.
It reads only two bundled fixture files and passed on local Perl 5.34.1.
Target CI must still prove the complete QEMU result. The installed-RPM
smoke checks grep, map, and callback behavior over an automatically cleaned
temporary file.

Successful PR CI artifacts alone do not prove public RPM repository publication.
