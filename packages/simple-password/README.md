<!-- SPDX-License-Identifier: Apache-2.0 -->
# simple-password

This directory packages upstream `https://github.com/ESzPa/spass` version `0.1.1` for openEuler 24.03 LTS SP3 on `riscv64`/RVA23.

Downstream release `3` adds the fixed-repository `vim-common` provider required by upstream's `xxd` source-generation command and configures explicit CMake source and out-of-source build directories while preserving the existing test behavior. The RISC-V build status remains `unknown` pending fresh CI evidence.

External source and patch licenses remain those of their respective upstream projects. The repository license only covers original packaging metadata, scripts, and documentation.
