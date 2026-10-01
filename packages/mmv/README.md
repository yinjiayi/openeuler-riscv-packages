<!-- SPDX-License-Identifier: Apache-2.0 -->
# mmv

This directory packages mmv 2.10 for openEuler 24.03 LTS SP3 on
`riscv64`/RVA23. The official GitHub release archive is fetched over HTTPS
and pinned by SHA-256. It includes generated Autotools, gengetopt, help2man
and Gnulib files, so the target build does not depend on bootstrapping from a
Git checkout.

The official README and current C source grant GPL-3.0-or-later. Frozen
distribution discovery rows disagree about the license; they are retained as
lineage and do not override the current upstream grant. The release registers
no automated test cases, so `%check` retains upstream `make check` and adds a
wildcard rename case. Installed smoke verifies the CLI version and move/copy
behavior. These tests do not by themselves prove native RISC-V hardware
behavior or repository publication. The repository's Apache-2.0 license
covers original packaging files only.
