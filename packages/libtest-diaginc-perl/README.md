<!-- SPDX-License-Identifier: Apache-2.0 -->
# perl-test-diaginc

This directory packages upstream `https://metacpan.org/dist/Test-DiagINC` version `0.010` for openEuler 24.03 LTS SP3 on `riscv64`/RVA23.

External source and patch licenses remain those of their respective upstream projects. The repository license only covers original packaging metadata, scripts, and documentation.

The signed CPAN release and Debian/Fedora lineage identify the package. The original Apache license is installed alongside the full upstream notices for the generated Makefile.PL (Dist::Zilla), prerequisite-report test (ReportPrereqs), and its embedded version grammar. Donor archives are pinned and are read only for notices.

All four upstream default test files and fixtures remain intact, including the taint-mode and lean-load checks. The installed smoke confirms that DiagINC reports a loaded module and preserves a deliberate nonzero exit status.
