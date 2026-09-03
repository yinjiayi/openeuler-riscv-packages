<!-- SPDX-License-Identifier: Apache-2.0 -->
# simple-mtpfs

This directory packages upstream `https://github.com/phatina/simple-mtpfs` version `0.4.0` release `3` for openEuler 24.03 LTS SP3 on `riscv64`/RVA23.

Downstream release `2` declares the fixed-repository Autoconf macro, pkg-config, FUSE, MTP, and USB providers required by upstream `configure.ac` while preserving the existing Autotools and test behavior. Release `3` raises the package timeout to 180 minutes after exact-head CI exhausted the former 60-minute budget while downloading the complete 241-package dependency transaction. The full Autotools build, test suite, and FUSE functionality remain enabled; the RISC-V build status remains `unknown` pending fresh CI evidence.

External source and patch licenses remain those of their respective upstream projects. The repository license only covers original packaging metadata, scripts, and documentation.
