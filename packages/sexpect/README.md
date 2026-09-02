<!-- SPDX-License-Identifier: Apache-2.0 -->
# sexpect

This directory packages upstream `https://github.com/clarkwang/sexpect` version `2.3.15` release `4` for openEuler 24.03 LTS SP3 on `riscv64`/RVA23.

Downstream release `3` passes the source and out-of-source build directories explicitly to CMake, supplies `procps-ng` for the process-state test, and shortens generated test socket paths to fit Linux `sockaddr_un.sun_path` while preserving the complete upstream suite and existing install behavior. Release `4` keeps the manual page out of the dynamic file manifest captured before RPM compresses manual pages and lists the installed compressed form explicitly. The source and patch SHA-256 digests remain unchanged, and the RISC-V build status remains `unknown` pending a successful exact-head CI build.

External source and patch licenses remain those of their respective upstream projects. The repository license only covers original packaging metadata, scripts, and documentation.
