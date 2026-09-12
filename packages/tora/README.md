<!-- SPDX-License-Identifier: Apache-2.0 -->
# tora

This directory packages upstream `https://github.com/tora-tool/tora` version `3.2` for openEuler 24.03 LTS SP3 on `riscv64`/RVA23.

The bundled ANTLR3 C++ runtime defines a `CyclicDFA` as immutable parser-table
state. GCC 14 rejects its copy constructor because it assigns const members
after initialization and rejects its assignment operator because those members
cannot be reassigned. The downstream patch initializes copies directly and
deletes assignment; generated tora parsers only construct static DFA objects.

The QEMU package build uses a 180-minute budget. In trusted exact-head run
34123431416, the dependency transaction completed successfully, CMake
configured, and compilation reached 85% without a compiler, linker, dependency,
or QEMU error before the 120-minute package deadline expired. Tora 3.2 does
not register tests with CTest, but its default debug build compiles the upstream
development test applications; packaging retains that build and the `%check`
CTest invocation rather than disabling either layer.

External source and patch licenses remain those of their respective upstream projects. The repository license only covers original packaging metadata, scripts, and documentation.

Release 11 adds the missing `QButtonGroup` include in `tosecurity.cpp`, where
the quota editor constructs the group and calls its methods. Exact-head CI
run `34230629837` exposed this separate translation-unit error after the
earlier browser include repair. The patch changes no quota logic, build
options, tests, or timeout budget; a replacement CI build is still required.
