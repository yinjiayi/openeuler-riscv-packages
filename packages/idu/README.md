<!-- SPDX-License-Identifier: Apache-2.0 -->
# idu

This directory packages upstream `https://github.com/MkP369/idu` version `0.1.0` for openEuler 24.03 LTS SP3 on `riscv64`/RVA23.

Exact-head Package CI run `34035013428` configured successfully in the source
directory, but `%cmake_build` looked for the absent
`riscv64-openEuler-linux-gnu` directory. Downstream release `2` explicitly
binds CMake to source directory `.` and `%{_vpath_builddir}`, so configure,
build, installation, and the retained CTest check share the same out-of-source
build directory. Exact-head run `34086501401` then compiled `idu` successfully
but proved that upstream defines no CMake install rule, so the buildroot stayed
empty. Release `3` installs the built executable explicitly while retaining the
same source, features, and CTest check. RISC-V build status is pending fresh
exact-head CI evidence.

External source and patch licenses remain those of their respective upstream projects. The repository license only covers original packaging metadata, scripts, and documentation.
