<!-- SPDX-License-Identifier: Apache-2.0 -->
# sexpect

This directory packages upstream `https://github.com/clarkwang/sexpect` version `2.3.15` for openEuler 24.03 LTS SP3 on `riscv64`/RVA23.

Downstream release `3` passes the source and out-of-source build directories explicitly to CMake, supplies `procps-ng` for the process-state test, and shortens generated test socket paths to fit Linux `sockaddr_un.sun_path` while preserving the complete upstream suite and existing install behavior. The source SHA-256 remains unchanged, and the RISC-V build status remains `unknown` pending fresh CI evidence.

External source and patch licenses remain those of their respective upstream projects. The repository license only covers original packaging metadata, scripts, and documentation.
