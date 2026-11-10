<!-- SPDX-License-Identifier: Apache-2.0 -->
# perl-object-event

This directory packages upstream `https://metacpan.org/dist/Object-Event` version `1.23` for openEuler 24.03 LTS SP3 on `riscv64`/RVA23.

The original Makefile.PL runs the default test suite without filters. The build does not use the network. Installation removes only generated Perl installer metadata; the RPM retains the original module, its manual, and the upstream README containing the license grant. The installed smoke checks that a registered callback receives the event payload.

External source and patch licenses remain those of their respective upstream projects. The repository license only covers original packaging metadata, scripts, and documentation.
