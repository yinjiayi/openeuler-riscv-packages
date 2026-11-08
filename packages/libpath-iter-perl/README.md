<!-- SPDX-License-Identifier: Apache-2.0 -->
# libpath-iter-perl

The frozen inventory's `libpath-iter-perl` key records Ubuntu source 0.2-4.
This package uses the official [Path-Iter 0.2](https://metacpan.org/dist/Path-Iter)
CPAN release. Its HTTPS archive SHA-256
`70883c387e224b7d07d1fea88dbd430bac3a94f5bf6f8e98beb718d1d6b4c0dd`
matches the publisher's `CHECKSUMS` entry. The archive has one root and only
regular files and directories, with no traversal or links. The module POD
and README grant redistribution under Perl 5 terms; no archive file has a
conflicting notice. The RPM uses the repository's Perl 5 dual-license SPDX
mapping, `GPL-1.0-or-later OR Artistic-1.0-Perl`.

The official openEuler 24.03 LTS SP3 RVA23 `everything` primary metadata,
SHA-256 `fdb1663ee6c803e8efcc83c19b7a1548f047f08abba8a52f5fe623b222064d1a`,
has neither `perl-Path-Iter` nor `perl(Path::Iter)`. It supplies File::Spec,
Test::More, Test::Pod 1.52 and Test::Pod::Coverage 1.10. This is a snapshot
check, not a guarantee about future repository contents.

The four unmodified upstream default test files include a 14-assertion
directory/symlink traversal test and POD checks. A fresh local source run
passed 16 assertions; `perlcritic.t` skipped under its explicit upstream
development-only policy, and `pod-coverage.t` skipped because the local Mac
lacks that optional provider. The target SPEC requires Test::Pod::Coverage,
so exact-head CI must prove that file runs on RISC-V. A staged vendor install
loaded Path::Iter 0.2 and passed temporary-directory iterator smoke locally.
The target RPM build, full default test result, installed smoke and physical
products remain unverified until exact-head CI. PR artifacts are not public
publication.
