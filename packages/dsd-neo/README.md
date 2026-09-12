<!-- SPDX-License-Identifier: Apache-2.0 -->
# dsd-neo

This directory packages upstream `https://github.com/arancormonk/dsd-neo` version `2.5.1` for openEuler 24.03 LTS SP3 on `riscv64`/RVA23.

External source and patch licenses remain those of their respective upstream projects. The repository license only covers original packaging metadata, scripts, and documentation.

Release 4 fixes a shared-library link failure observed in the RVA23 build:
crypto calls the bit-packing utility, while the utility was compiled only into
core, which itself depends on crypto. The downstream CMake patch assigns that
utility to crypto; core retains access through its existing public dependency.
The full upstream CTest suite remains enabled.

Release 5 also undefines four ncurses window-accessor macros inside the
printer-helper test so its existing deterministic function stubs compile.
The test assertions and production UI behavior are unchanged.
