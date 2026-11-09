<!-- SPDX-License-Identifier: Apache-2.0 -->
# perl-io-capture

This directory packages upstream `https://metacpan.org/dist/IO-Capture` version `0.05` for openEuler 24.03 LTS SP3 on `riscv64`/RVA23.

External source and patch licenses remain those of their respective upstream projects. The repository license only covers original packaging metadata, scripts, and documentation.

- The exact signed archive is named `IO-Capture-0.05.tar.gz` and its primary module and MakeMaker build identify 0.05. Fedora 44 GA ships 0.05-49.fc44; Debian 0.05-6 references the identical upstream archive SHA-256. The original META.yml and its MetaCPAN metadata still say 0.04. They remain unmodified.
- The package includes verbatim copies of all four original same-Perl POD notices, in addition to preserving the installed POD and modules.
- The full original default harness runs offline. The installed smoke checks separate stdout and stderr capture and restoration of the original handles.
