<!-- SPDX-License-Identifier: Apache-2.0 -->
# simdzone

This directory packages upstream `https://github.com/NLnetLabs/simdzone` version `0.2.4` release `2` for openEuler 24.03 LTS SP3 on `riscv64`/RVA23.

The verified release archive contains its CMake project at the archive root, and the enabled test tree requires cmocka. Release `2` declares `libcmocka-devel` and explicitly binds CMake to source directory `.` and `%{_vpath_builddir}`, so configuration, build, installation, and CTest use the same out-of-tree build without disabling tests or parser functionality.

External source and patch licenses remain those of their respective upstream projects. The repository license only covers original packaging metadata, scripts, and documentation.
