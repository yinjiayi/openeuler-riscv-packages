<!-- SPDX-License-Identifier: Apache-2.0 -->
# libdns-zoneparse-perl

This directory packages upstream `https://metacpan.org/dist/DNS-ZoneParse` version `1.10` for openEuler 24.03 LTS SP3 on `riscv64`/RVA23.

External source and patch licenses remain those of their respective upstream projects. The repository license only covers original packaging metadata, scripts, and documentation.

The original README and module retain the author's Perl dual grant; both
official full license texts are shipped. The fixed archive matches PAUSE
and Debian stable's original bytes.

All six upstream default test files are retained. Installed smoke exercises
a synthetic local zone's A and SOA records through parse, serialization and
reparse; neither tests nor smoke perform DNS lookups.
