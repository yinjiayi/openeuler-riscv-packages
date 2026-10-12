<!-- SPDX-License-Identifier: Apache-2.0 -->
# pstack

This directory packages upstream `https://github.com/peadar/pstack` version `2.17` for openEuler 24.03 LTS SP3 on `riscv64`/RVA23.

External source and patch licenses remain those of their respective upstream projects. The repository license only covers original packaging metadata, scripts, and documentation.

Downstream release 2 escapes `find`'s `%P` format as `%%P` in the SPEC so RPM macro expansion preserves the intended relative-path manifest expression. Release 3 uses openEuler's `%cmake_conf` macro so configuration creates `%{_vpath_builddir}`, the directory subsequently consumed by `%cmake_build`, `%cmake_install`, and `%check`. Fresh exact-head CI is required before claiming a successful RISC-V build.
