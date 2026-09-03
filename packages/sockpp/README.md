<!-- SPDX-License-Identifier: Apache-2.0 -->
# sockpp

This directory packages upstream `https://github.com/fpagliughi/sockpp` version `1.0.0` for openEuler 24.03 LTS SP3 on `riscv64`/RVA23.

Downstream release `3` retains the Catch2 development provider and all upstream registered unit tests while raising the package timeout to 180 minutes. Exact-head CI resolved the complete 124-package, 170 MB dependency transaction, but the former 60-minute budget expired during dependency downloads before `rpmbuild` began; it therefore provided no package compilation or test result. Test and library functionality remain enabled, the source SHA-256 is unchanged, and the RISC-V build status remains `unknown` pending fresh CI evidence.

External source and patch licenses remain those of their respective upstream projects. The repository license only covers original packaging metadata, scripts, and documentation.
