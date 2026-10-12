<!-- SPDX-License-Identifier: Apache-2.0 -->
# Data::Pond 0.006

The frozen Ubuntu `libdata-pond-perl` 0.006-1 inventory key maps to official
[Data-Pond 0.006](https://metacpan.org/dist/Data-Pond). Publisher CHECKSUMS
and the independently downloaded 19,542-byte HTTPS release agree on SHA-256
`9c0efa899e7cd575457c6f6894573e7bf0f645d4099e4ab64b6836540f5f403e`.
The archive has only regular files and directories under one top-level tree.

The publisher's distribution-level `META.json` and generated `Build.PL`
declare Perl 5 licensing. The README and installed `Data::Pond` POD name both
copyright holders, PhotoBox Ltd and Andrew Main (Zefram), and explicitly grant
same-Perl redistribution. `lib/Data/Pond.xs` and the small bundled
`inc/Local/ModuleBuild.pm` build shim carry no separate notice or contrary
attribution; the distribution-level grant covers them. No third-party library
is bundled. The RPM license expression reflects Perl's GPL-or-Artistic terms.

The official openEuler 24.03 LTS SP3 riscv64/RVA23 primary has no
`perl-Data-Pond` or `perl(Data::Pond)` provider. It supplies the riscv64 GCC
14.3.1, Perl development and Perl runtime ABI 5.38.0, and unique providers
for Module::Build, ExtUtils::CBuilder, Params::Classify, and XSLoader.

Unmodified upstream tests contain seven functional files with 493 assertions,
including non-`_pp` and forced pure-Perl `_pp` pairs; two author-only POD files
self-skip without `AUTHOR_TESTING`. A preliminary macOS run inadvertently
loaded only the fallback because hardened `dlopen` rejected a relative
`blib/arch` path. Re-running the unchanged suite with absolute `PERL5LIB`
confirmed the XS entry point is loaded and all 493 assertions pass. `%check`
explicitly verifies the XS entry point before the full upstream suite.
Target CI must prove the riscv64 XS build, unchanged tests, physical RPM/SRPM,
DNF install, and installed XS read/write smoke. PR CI is not publication.
