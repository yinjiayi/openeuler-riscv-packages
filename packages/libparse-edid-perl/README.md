<!-- SPDX-License-Identifier: Apache-2.0 -->
# perl-parse-edid

This directory packages upstream `https://metacpan.org/dist/Parse-EDID` version `1.0.7` for openEuler 24.03 LTS SP3 on `riscv64`/RVA23.

External source and patch licenses remain those of their respective upstream projects. The repository license only covers original packaging metadata, scripts, and documentation.

The fixed CPAN archive matches MetaCPAN and the PAUSE checksum signed at the recorded signing time. Fedora 44 GA and Debian lineage establish the package identity; no downstream packaging was executed. The RPM ships the unmodified module and the original full GPL license.

The upstream default harness and all 63 fixtures are retained. The optional Test::Kwalitee file keeps its own skip when the dependency is unavailable; POD and POD coverage run. The separate installed smoke parses a synthetic binary EDID with a known manufacturer and product ID.
