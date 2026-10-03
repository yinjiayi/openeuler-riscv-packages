# Data::Section::Simple

Data::Section::Simple 0.07 extracts named text sections from Perl DATA handles.
Its official CPAN 11,479-byte archive matches the author CHECKSUMS SHA-256.
The frozen `libdata-section-simple-perl` Ubuntu lineage is 0.07-4; openSUSE's
0.70.0 packaging number is not claimed as an upstream release.

Bundled LICENSE, README and the module POD grant Perl GPL/Artistic terms.
Independent review of all 17 regular files found no restricted third-party
fixture; all five tests use short self-contained generated data. The archive
contains 22 ordinary entries under one root. However, the module's credited
Mojo-derived extraction code has an additional historical origin contract,
described below; Perl-only metadata was incomplete accounting, not proof of
absent permission. The verified official target primary metadata SHA-256
`fdb1663ee6c803e8efcc83c19b7a1548f047f08abba8a52f5fe623b222064d1a`
has neither the RPM name nor module provider and supplies the test dependencies.

## Mojo origin notice supplement

Official [Mojo commit 3387874bbd0e8e8eadc8c8c2b9bb6903e7164fb6](https://github.com/mojolicious/mojo/tree/3387874bbd0e8e8eadc8c8c2b9bb6903e7164fb6),
dated 2010-02-26, identifies the credited parser's historical origin. Its
`lib/Mojo/Command.pm:89-123` contains the original DATA parser and Sebastian
Riedel 2008-2010 copyright; `Makefile.PL:24` explicitly declares `artistic_2`.
Its [LICENSE](https://github.com/mojolicious/mojo/blob/3387874bbd0e8e8eadc8c8c2b9bb6903e7164fb6/LICENSE)
is the Artistic License 2.0, 8,894 bytes, SHA-256
`685e534b60d4e2b4fbb1a259a83b5a86e877a919bbb9efc95994276f706a3a71`.
Source1 retrieves exactly those bytes over immutable HTTPS, independently
verifies the pin, and copies them unchanged to installed `LICENSE.Mojo`.
The schema's `upstream-release` source kind denotes this official source
supplement; its version `2.0` is the license version, not a claim that the
historical commit is a stable Mojo software release. It is not a test dependency.

The package-only documentation patch adds `MOJO-PROVENANCE`, recording the
adapted parser's differences, Data::Section::Simple's distinct module namespace,
and non-overlapping installation. No Mojo file or executable is replaced;
the standard Mojo package can coexist. This documents the Artistic-2.0
section 4(b) separately named/non-interfering installation path. The SPDX
expression conservatively records the upstream Perl grant **and** the original
Artistic-2.0 terms. The original CPAN archive, module, copyright notices,
fixtures and every functional test remain untouched; no source repack or
relicensing assertion is made. This is a license-notice/derivative-provenance
repair supported by an existing official grant, not legal certainty.

Original `LICENSE`, exact `LICENSE.Mojo` and `MOJO-PROVENANCE` are installed
as license material. Smoke checks their complete SHA-256 bytes and the original
installed module, in addition to functional behavior. The notice is 1,831 bytes,
SHA-256 `9b1bcdbe80a754a21699892287bbf9a8920fa62e64a0086a2c240887a125e64e`.

## Validation boundary

`%check` runs all five default files with `RELEASE_TESTING=1`, including upstream
release POD validation. Installed smoke reads two sections through functional
and object interfaces and checks missing names. Source verify-only and local
metadata gates are separate from locked openEuler SP3 riscv64 RVA23 CI. No
local RPM/QEMU build or public publication is claimed. Historical release-1
CI at `5bba576ccb8d0b41531a2ced3f3260d2ad0185f8` passed five files/nine assertions
with no visible skip, but does not prove release-2 notice installation. Keep
this PR draft until root review, all exact-current-head hosted checks, complete
target tests and installed-byte smoke are independently audited.
