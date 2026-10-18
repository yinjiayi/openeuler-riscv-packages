<!-- SPDX-License-Identifier: Apache-2.0 -->
# libfile-find-wanted-perl

The frozen inventory's exact `libfile-find-wanted-perl` key maps to the
latest official [File-Find-Wanted 1.00](https://metacpan.org/dist/File-Find-Wanted).
The CPAN `CHECKSUMS` entry and downloaded HTTPS archive both have SHA-256
`3d41caadd1d4df785ef3eb269c667c656d864df79a490137f9cab33b8d244886`.
The archive's 15 entries form one top-level tree without traversal paths,
links or special files. Both `README.md` and `Wanted.pm` explicitly grant
Artistic-2.0 redistribution and modification, resolving the frozen automated
`license-blocked` and `unverified-upstream` decisions for this release.

The official openEuler 24.03 LTS SP3 RVA23 `everything` primary metadata,
`primary.xml.zst` SHA-256
`fdb1663ee6c803e8efcc83c19b7a1548f047f08abba8a52f5fe623b222064d1a`,
contains neither `perl-File-Find-Wanted` nor `perl(File::Find::Wanted)`.
It contains `perl-Test-Pod` 1.52 and `perl-Test-Pod-Coverage` 1.10, which
are included as build requirements so the optional upstream POD tests run
on the target. This is a snapshot check, not a guarantee about future state.

`%check` retains all four default upstream test files: load, functional
directory search, POD and POD coverage. The functional test only reads
fixtures from the fresh source tree. On the local Perl 5.34.1 host, the
load, functional and POD files passed (five assertions), while POD coverage
was explicitly skipped because that local module is absent. The target CI
must prove the complete four-file run. The installed-RPM smoke searches
temporary files and cleans them automatically.

Successful PR CI artifacts alone do not prove public RPM repository publication.
