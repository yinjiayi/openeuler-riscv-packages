<!-- SPDX-License-Identifier: Apache-2.0 -->
# perl-return-multilevel

This directory packages upstream `https://metacpan.org/dist/Return-MultiLevel` version `0.08` for openEuler 24.03 LTS SP3 on `riscv64`/RVA23.

External source and patch licenses remain those of their respective upstream projects. The repository license only covers original packaging metadata, scripts, and documentation.

The original full same-Perl license is installed alongside notices from exact Dist::Zilla and Plicease generator releases. These pinned archives are read only for notices; neither generator is run.

All four upstream default test files are retained. The recipe does not override upstream backend selection: the pure Perl backend is selected when optional Scope::Upper is unavailable. The installed smoke exercises nested callback unwinding and verifies its return values.
