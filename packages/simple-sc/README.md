<!-- SPDX-License-Identifier: Apache-2.0 -->
# simple-sc

This directory packages upstream `https://github.com/directmusic/simple-sc` version `0.1.2` for openEuler 24.03 LTS SP3 on `riscv64`/RVA23.

Downstream release `2` declares the fixed-repository pkg-config, PipeWire, D-Bus, portal, FFmpeg, and zlib providers required by upstream CMake. Release `3` uses one explicit out-of-source CMake directory for configure, build, install, and check while preserving the existing feature set. The source SHA-256 remains unchanged, and the RISC-V build status remains `unknown` pending fresh CI evidence.

External source and patch licenses remain those of their respective upstream projects. The repository license only covers original packaging metadata, scripts, and documentation.
