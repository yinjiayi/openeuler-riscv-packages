<!-- SPDX-License-Identifier: Apache-2.0 -->
# qucs-rflayout

This directory packages upstream `https://github.com/thomaslepoix/Qucs-RFlayout` version `2.1.2` for openEuler 24.03 LTS SP3 on `riscv64`/RVA23.

Downstream release `2` matches the pinned archive's exact `Qucs-RFlayout-2.1.2` source root, declares the fixed-repository Qt 6 and OpenGL development providers, and uses upstream's `check` target so its excluded unit-test executable is built before CTest. GUI and test functionality remain enabled, the source SHA-256 is unchanged, and the RISC-V build status remains `unknown` pending fresh CI evidence.

External source and patch licenses remain those of their respective upstream projects. The repository license only covers original packaging metadata, scripts, and documentation.
