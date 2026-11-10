<!-- SPDX-License-Identifier: Apache-2.0 -->
# perl-sub-override

This directory packages upstream `https://metacpan.org/dist/Sub-Override` version `0.12` for openEuler 24.03 LTS SP3 on `riscv64`/RVA23.

The original Makefile.PL runs the unfiltered default suite. The RPM keeps the original module, manual and license grant in the module POD, and omits only generated Perl installer metadata. The installed smoke replaces a named subroutine and then checks that its original behavior is restored.

External source and patch licenses remain those of their respective upstream projects. The repository license only covers original packaging metadata, scripts, and documentation.
