<!-- SPDX-License-Identifier: Apache-2.0 -->
# libtest-deep-fuzzy-perl

This directory packages upstream `https://metacpan.org/release/KARUPA/Test-Deep-Fuzzy-0.01` version `0.01` for openEuler 24.03 LTS SP3 on `riscv64`/RVA23.

External source and patch licenses remain those of their respective upstream projects. The repository license only covers original packaging metadata, scripts, and documentation.

The CPAN author release is pinned by SHA-256 and retains its original Perl 5
dual-license terms. The distributed `Build.PL` is the
[Minilla v3.0.4 template](https://github.com/tokuhirom/Minilla/blob/6ef4c2f1ab7eafe5b143b11c0e0fb7e330aa06c9/lib/Minilla/ModuleMaker/ModuleBuildTiny.pm)
rendered without external binary requirements. The exact generator's license
is pinned separately and included with the original distribution license.

The target uses published `perl(Math::Round)` 0.08 and the distro Perl,
Module::Build::Tiny, Test::Deep, Test::More and core modules. The normal
`Build test --verbose` runs both original test files without modifications.
The installed smoke checks both an equivalent and a different rounding
bucket. No RISC-V patch or native-only behavior is assumed; target evidence
comes from CI.
