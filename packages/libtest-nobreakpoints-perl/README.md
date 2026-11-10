<!-- SPDX-License-Identifier: Apache-2.0 -->
# perl-test-nobreakpoints

This directory packages upstream `https://metacpan.org/dist/Test-NoBreakpoints` version `0.17` for openEuler 24.03 LTS SP3 on `riscv64`/RVA23.

External source and patch licenses remain those of their respective upstream projects. The repository license only covers original packaging metadata, scripts, and documentation.

The official release archive is pinned by SHA-256 in `sources.yaml`. `%check` runs the unchanged upstream default suite with verbose output. Host preflight with the optional Test::NoWarnings fixture observed 11 files and 108 assertions passing, with the upstream placeholder and four release-only whole-file skips. The SPEC requests that available test dependency so those four extra checks also run on target. This is not target build evidence.

The installed smoke test checks that `Test::NoBreakpoints` accepts a clean Perl fixture. Target RPM/SRPM, original tests, installation and smoke results must be verified in CI before acceptance.
