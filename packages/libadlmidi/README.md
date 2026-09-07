<!-- SPDX-License-Identifier: Apache-2.0 -->
# libadlmidi

This directory packages upstream `https://github.com/Wohlstand/libADLMIDI` version `1.6.1` for openEuler 24.03 LTS SP3 on `riscv64`/RVA23.

External source and patch licenses remain those of their respective upstream projects. The repository license only covers original packaging metadata, scripts, and documentation.

Packaging release 2 enters the case-sensitive `libADLMIDI-1.6.1` top-level directory recorded in the pinned upstream archive before running the unchanged CMake build and test suite.

Packaging release 3 configures CMake in the RPM macro build directory used by the build, install, and check phases, and enables upstream's `WITH_UNIT_TESTS` CTest suite.
