<!-- SPDX-License-Identifier: Apache-2.0 -->
# libomemo

This directory packages upstream `https://github.com/gkdr/libomemo` version `0.8.1` for openEuler 24.03 LTS SP3 on `riscv64`/RVA23.

Downstream release `2` declares the CMocka, GLib, libgcrypt, Mini-XML, and SQLite pkg-config providers, keeps all three upstream CMocka executables enabled, and configures in the out-of-tree directory expected by the openEuler CMake macros. The package-local patch ports the private implementation from Mini-XML 3 callbacks to the parallel-installable Mini-XML 4 API supplied by the immutable project repository; the public libomemo API is unchanged. The source SHA-256 remains unchanged, and RISC-V build status remains `unknown` pending fresh exact-head CI evidence.

External source and patch licenses remain those of their respective upstream projects. The repository license only covers original packaging metadata, scripts, and documentation.
