<!-- SPDX-License-Identifier: Apache-2.0 -->
# perl-data-properties

This directory packages upstream `https://metacpan.org/dist/Data-Properties` version `1.07` for openEuler 24.03 LTS SP3 on `riscv64`/RVA23.

External source and patch licenses remain those of their respective upstream projects. The repository license only covers original packaging metadata, scripts, and documentation.

- The signed exact 1.07 archive re-releases 0.02, not the incompatible 1.05. It includes the original author's Apache grant; Fedora 44 and FreeBSD's exact 1.07 archive record independently identify Apache-2.0. The archive's MetaCPAN metadata still says `unknown`; the RPM preserves upstream `LICENSE` verbatim and the complete official Apache-2.0 terms.
- The original default Perl test and original properties fixture run unchanged during the offline build.
- The installed smoke exercises continued lines, empty values and a read/write/reload round trip.
