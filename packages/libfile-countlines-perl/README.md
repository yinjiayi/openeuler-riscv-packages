<!-- SPDX-License-Identifier: Apache-2.0 -->
# libfile-countlines-perl

The frozen inventory's exact `libfile-countlines-perl` key maps to official
[File-CountLines v0.0.3](https://metacpan.org/dist/File-CountLines). The CPAN
HTTPS archive and `CHECKSUMS` entry both report SHA-256
`cfd97cce7c9613e4e569d47874a2b5704f1be9eced2f0739c870725694382a62`.
All 13 archive entries remain under one top-level tree, with no traversal
paths, links, or special files.

The frozen discovery index carried a `license-blocked` flag. This release's
`README` and module POD explicitly permit use, redistribution, and modification
under the same terms as Perl, while `META.yml` and `Build.PL` declare `perl`.
The RPM license expression `GPL-1.0-or-later OR Artistic-1.0-Perl` maps those
Perl 5 dual terms; no conflicting bundled code was found. The upstream release
asks for a new maintainer, so this compatibility package does not imply active
upstream maintenance.

The official openEuler 24.03 LTS SP3 RVA23 `everything` primary metadata,
`primary.xml.zst` SHA-256
`fdb1663ee6c803e8efcc83c19b7a1548f047f08abba8a52f5fe623b222064d1a`,
has neither a `perl-File-CountLines` RPM nor a `perl(File::CountLines)` provider.
It contains `perl-Test-Pod` 1.52, explicitly required for the optional upstream
POD test, so neither default test file needs to be skipped. This snapshot
check does not guarantee future repository contents.

`%check` retains both default upstream test files. They passed all 22 tests
on local Perl 5.34.1. The target CI must still prove the complete QEMU run.
The installed-RPM smoke counts both native and CRLF line breaks in a temporary
file.

Successful PR CI artifacts alone do not prove public RPM repository publication.
