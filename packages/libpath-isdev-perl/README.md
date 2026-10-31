<!-- SPDX-License-Identifier: Apache-2.0 -->
# libpath-isdev-perl

The frozen inventory key `libpath-isdev-perl` records Ubuntu source
1.001003-3. This package uses the official [Path-IsDev 1.001003](https://metacpan.org/dist/Path-IsDev)
CPAN release. Its HTTPS archive SHA-256
`37d66bfe205d7916824a46ad6290b8fb170fc602c16f8dc8169576f2ad682949`
matches publisher `CHECKSUMS`. The archive has one root, regular files and
directories only, and no traversal paths or links.

The distribution `LICENSE` grants GPL version 1 or later, or Artistic License
1.0, as Perl 5 terms; all 27 shipped Perl modules repeat that grant. No
conflicting source or corpus notice was found. The RPM metadata uses
`GPL-1.0-or-later OR Artistic-1.0-Perl`.

The official openEuler 24.03 LTS SP3 RVA23 `everything` primary metadata,
SHA-256 `fdb1663ee6c803e8efcc83c19b7a1548f047f08abba8a52f5fe623b222064d1a`,
has neither this RPM nor `perl(Path::IsDev)`. It uniquely supplies
`perl(File::HomeDir)=1.006` via `perl-File-HomeDir` 0:1.006-3.oe2403sp3,
and also supplies the other declared runtime/test modules. This is a
snapshot check, not a guarantee about future repository contents.

All 39 upstream default test files remain unchanged. A fresh local Perl
5.34 run **failed** 11 files and 18 assertions because the Mac lacks
File::HomeDir; the only observed exception was `Can't locate File/HomeDir.pm`,
with subsequent missing assertions caused by that exception. The SPEC
declares the verified target provider as both a build and runtime dependency.
The first PR head built successfully on the target with all 39 default test
files and 111 assertions passing, but its installed smoke failed after DNF
installed the RPM: `Path::IsDev::Result` could not load `Path::Tiny`. The
second head installed `Path::Tiny` and again passed all 39 files/111 assertions,
but installed smoke then found `Module::Runtime` absent. A complete shipped
source scan found four external lazy `require` modules: `File::HomeDir`,
`Path::Tiny`, `Module::Runtime`, and `Scalar::Util`. RPM's generated Requires
missed these imports, so the SPEC explicitly declares all four, backed by
providers in the checksum-bound official target repository. The next head
still requires exact-head installed smoke and physical-product verification.
PR artifacts are not public publication.
