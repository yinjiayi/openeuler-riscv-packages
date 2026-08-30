<!-- SPDX-License-Identifier: Apache-2.0 -->
# tora

This directory packages upstream `https://github.com/tora-tool/tora` version `3.2` for openEuler 24.03 LTS SP3 on `riscv64`/RVA23.

The bundled ANTLR3 C++ runtime defines a `CyclicDFA` as immutable parser-table
state. GCC 14 rejects its copy constructor because it assigns const members
after initialization and rejects its assignment operator because those members
cannot be reassigned. The downstream patch initializes copies directly and
deletes assignment; generated tora parsers only construct static DFA objects.

External source and patch licenses remain those of their respective upstream projects. The repository license only covers original packaging metadata, scripts, and documentation.
