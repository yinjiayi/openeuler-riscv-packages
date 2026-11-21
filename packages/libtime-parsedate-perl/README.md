<!-- SPDX-License-Identifier: Apache-2.0 -->
# libtime-parsedate-perl

This directory packages upstream `https://metacpan.org/dist/Time-ParseDate` version `2026.033` for openEuler 24.03 LTS SP3 on `riscv64`/RVA23.

External source and patch licenses remain those of their respective upstream projects. The repository license only covers original packaging metadata, scripts, and documentation.

The fixed CPAN release includes nine original vendored build helpers.
Their source matches the reviewed Module::Install 1.21 and ReadmeFromPod
0.30 donors after removing POD, line directives and blank lines. The
package preserves both original donor notices and both Perl license texts.
The vendor helpers themselves are not installed by the binary RPM.

The original tests are unmodified. The target supplies Test::MockTime and
timezone data for the tests that simulate daylight-saving time. The
installed smoke separately checks two fixed epoch conversions.
