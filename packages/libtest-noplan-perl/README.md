<!-- SPDX-License-Identifier: Apache-2.0 -->
# perl-test-noplan

This directory packages upstream `https://metacpan.org/dist/Test-NoPlan` version `0.0.6` for openEuler 24.03 LTS SP3 on `riscv64`/RVA23.

External source and patch licenses remain those of their respective upstream projects. The repository license only covers original packaging metadata, scripts, and documentation.

The official source archive and source root retain the v0.0.6 spelling; the RPM version is normalized to 0.0.6. The original README contains the same-Perl license. The package retains the exact Module::Build::Compat notice for the shipped but unused Makefile.PL, and builds with the original hand-written Build.PL.

All original default tests are retained, with dependencies for both POD checks supplied. The install phase disables Module::Build's packlist. The installed smoke uses fixture files to check fixed-plan acceptance and explicit no_plan detection.
