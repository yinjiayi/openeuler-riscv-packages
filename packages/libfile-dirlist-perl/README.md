<!-- SPDX-License-Identifier: Apache-2.0 -->
# libfile-dirlist-perl

The frozen inventory's exact `libfile-dirlist-perl` key maps to the official
[File-DirList 0.05](https://metacpan.org/dist/File-DirList) release. The CPAN
HTTPS archive SHA-256 is
`993b7d7662e55798448a1edaccb9abd281d2bd23be7eab99f569b8e2962d3bc3`,
matching its official publisher `CHECKSUMS` entry. The seven archive entries
are ordinary files under one safe top-level directory.

The main module POD and README expressly grant redistribution and modification
under Perl 5.8.4-or-later terms. Legacy `META.yml` says `license: unknown`, and
the README retains a stale template line before the explicit grant; neither
metadata field is represented as the grant itself. The package declares the
Perl GPL/Artistic alternative and retains the upstream source unchanged.

The official openEuler 24.03 LTS SP3 RVA23 `everything` primary metadata,
`primary.xml.zst` SHA-256
`fdb1663ee6c803e8efcc83c19b7a1548f047f08abba8a52f5fe623b222064d1a`,
has neither a `perl-File-DirList` RPM nor a `perl(File::DirList)` provider, and
supplies the required core and test modules. This snapshot does not guarantee
future repository contents.

The unmodified default upstream test passed one file/two assertions on local
Perl 5.34.1. Its original test prints the entries of `HOME` to stderr, so
`%check` points `HOME` at an empty private directory; no assertions are
removed. Installed-RPM smoke separately checks the module/provider, version,
and sorted names from a private temporary fixture. Target QEMU CI and public
RPM/SRPM publication are unverified until exact-head evidence exists.
