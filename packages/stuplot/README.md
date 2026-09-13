<!-- SPDX-License-Identifier: Apache-2.0 -->
# stuplot

This directory packages upstream `https://github.com/Friendships6666/StuPlot` version `1.0.0` release `4` for openEuler 24.03 LTS SP3 on `riscv64`/RVA23.

Downstream release `3` matches the SPEC source root to the pinned archive's exact `StuPlot-1.0.0` top-level directory and configures explicit CMake source and out-of-source build directories. Release `4` disables the empty debuginfo subpackage because this header-only library installs headers and CMake metadata rather than compiled ELF objects. All four upstream examples remain part of the build, and no source, feature, or check command is changed. The RISC-V build status remains `unknown` pending a successful exact-head CI build.

External source and patch licenses remain those of their respective upstream projects. The repository license only covers original packaging metadata, scripts, and documentation.
