<!-- SPDX-License-Identifier: Apache-2.0 -->
# libfile-finder-perl

The frozen inventory's exact `libfile-finder-perl` key maps to official
[File-Finder 1.01](https://metacpan.org/dist/File-Finder). The CPAN HTTPS
archive and its official `CHECKSUMS` entry both have SHA-256
`2b6abd64354e76c5c2e5b37a34228af2d807f6ed4ab7070b116b6b448265fb87`.
Every archive path stays under one top-level tree and no special file type
is included. Both module PODs expressly grant redistribution and modification
under Perl's terms; the old inventory's `unverified-upstream` decision was
rechecked against the actual archive.

The official openEuler 24.03 LTS SP3 RVA23 `everything` primary metadata,
`primary.xml.zst` SHA-256
`fdb1663ee6c803e8efcc83c19b7a1548f047f08abba8a52f5fe623b222064d1a`,
has no `perl-File-Finder` RPM or `perl(File::Finder)` provider, but does
provide the required Text::Glob and File::Find::Rule packages. This snapshot
check does not guarantee future repository contents.

`%check` retains all eight default upstream `t` files. Local Perl 5.34.1
ran five files/100 assertions successfully; three files reported upstream
conditional skips: distribution tests require Test::Distribution plus
`TEST_VERBOSE`, POD coverage requires Test::Pod::Coverage plus `TEST_VERBOSE`,
and POD tests require `TEST_VERBOSE`. These are source-defined conditions,
not removed tests or a claim that their assertions passed. Installed-RPM
smoke exercises both modules and searches a private temporary tree. Target
QEMU results remain unverified until exact-head CI, and PR artifacts alone
do not establish public RPM repository publication.
