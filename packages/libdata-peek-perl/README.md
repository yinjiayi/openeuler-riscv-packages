<!-- SPDX-License-Identifier: Apache-2.0 -->
# Data::Peek 0.54

The frozen Ubuntu `libdata-peek-perl` 0.54-1 inventory key maps to official
stable [Data-Peek 0.54](https://metacpan.org/dist/Data-Peek). Publisher
CHECKSUMS and the independently downloaded 143,524-byte HTTPS archive agree
on SHA-256 `4dbf2205d43fb7d963ba29902cd563a5ea6c3c6bb49a9493c40ce8b0f8572980`.
The archive has one top-level tree and only regular files and directories.

The release README, installed `Peek.pm`, and `Peek.xs` grant same-Perl
redistribution from H.Merijn Brand. Bundled Devel::PPPort `ppport.h` credits
Marcus Holland-Moritz, Paul Marquess, and Kenneth Albanowski and separately
grants the same terms. The generated optional `DP.pm` source in `Makefile.PL`
also carries a same-Perl grant. No contrary per-file notice was found.

The official openEuler 24.03 LTS SP3 riscv64/RVA23 primary has no
`perl-Data-Peek` or `perl(Data::Peek)` provider. It uniquely supplies GCC,
Perl development and Perl runtime ABI 5.38.0, Data::Dumper, XSLoader,
Test::Warnings, Test::Pod, Test::Pod::Coverage, and Perl::Tidy.

Upstream `AUTOMATED_TESTING=1` is its noninteractive build mode: it suppresses
only an optional `DP` alias prompt; this release contains no `xt/` directory
and still runs every unchanged `t/*.t` default file. The local macOS run
passed 15 files and 272 assertions, but `t/01_pod.t` self-skipped because
local Test::Pod::Coverage was absent and the optional Perl::Tidy branch was
unavailable. The target SPEC hard-requires both, verifies a genuine DPeek XS
entry point and real output, then requires all 15 files, at least 272
assertions, and no skips. Exact-head target CI must also build physical
RPM/SRPM products, DNF-install the RPM, and pass installed XS peek/display
smoke. PR CI is not publication.
