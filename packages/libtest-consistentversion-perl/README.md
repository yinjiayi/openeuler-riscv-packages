<!-- SPDX-License-Identifier: Apache-2.0 -->
# Test::ConsistentVersion

This directory packages upstream `https://metacpan.org/dist/Test-ConsistentVersion` version `0.3.1` for openEuler 24.03 LTS SP3 on `riscv64`/RVA23.

External source and patch licenses remain those of their respective upstream projects. The repository license only covers original packaging metadata, scripts, and documentation.

The fixed CPAN archive is checked against both the publisher's CHECKSUMS and MetaCPAN. The unchanged upstream README contains the original Perl-terms grant and is installed as the license notice. No patches are used.

`./Build test verbose=1` retains the complete upstream default harness: eight original test files, four author-only whole-file skips when `TEST_AUTHOR` is unset, and seven executed assertions. Target RPM and installed-module proof are separate from the host tests.
