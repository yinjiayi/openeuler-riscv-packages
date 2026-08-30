<!-- SPDX-License-Identifier: Apache-2.0 -->
# simpleini

This directory packages upstream `https://github.com/brofield/simpleini` version `4.26` for openEuler 24.03 LTS SP3 on `riscv64`/RVA23.

Release 2 configures the upstream-supported system GoogleTest path instead of
downloading GoogleTest during CMake configuration. The system package provides
the same GoogleTest 1.14.0 version pinned by upstream, and the registered CTest
suite remains enabled and runs during `%check`.

External source and patch licenses remain those of their respective upstream projects. The repository license only covers original packaging metadata, scripts, and documentation.
