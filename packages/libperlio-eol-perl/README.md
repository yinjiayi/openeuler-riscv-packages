<!-- SPDX-License-Identifier: Apache-2.0 -->
# libperlio-eol-perl

This directory packages upstream `https://metacpan.org/dist/PerlIO-eol` version `0.19` for openEuler 24.03 LTS SP3 on `riscv64`/RVA23.

The authorized CPAN archive in `sources.yaml` matches the publisher
CHECKSUMS and MetaCPAN release metadata. The full original LICENSE and
README retain the Audrey Tang grant and the Randy Kobes notices.
Debian stable 0.19-1 establishes naming lineage only.

The architecture-specific package uses upstream MakeMaker and retains
both default test files and their explicit trailing-CR TODO. Installed
smoke loads the XS layer and checks LF normalization of mixed CRLF, CR,
and LF input. Native host checks do not replace target CI.

External source and patch licenses remain those of their respective upstream projects. The repository license only covers original packaging metadata, scripts, and documentation.
