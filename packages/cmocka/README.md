<!-- SPDX-License-Identifier: Apache-2.0 -->
# cmocka

This directory packages the official cmocka 2.0.2 release for openEuler 24.03 LTS SP3 on `riscv64`/RVA23. CI fetches and verifies the pinned archive with networking enabled, builds the shared library and development files, and runs the complete 80-test CTest suite. QEMU user mode reaches test 9 after eight passes and then traps with `SIGILL`, so the unchanged suite requires native RISC-V validation.

External source and patch licenses remain those of their respective upstream projects. The repository license only covers original packaging metadata, scripts, and documentation.
