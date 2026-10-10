<!-- SPDX-License-Identifier: Apache-2.0 -->
# gawk

This directory packages GNU gawk 5.4.1 for openEuler 24.03 LTS SP3 on `riscv64`/RVA23. The network-enabled build enables MPFR and readline, installs the awk compatibility link and extension header, and runs `make check` in full. Under QEMU user mode, the complete suite reproducibly formats unassigned array values as numeric zero in six tests at both the default optimization and `-O1`; the unchanged suite therefore requires native RISC-V validation.

External source and patch licenses remain those of their respective upstream projects. The repository license only covers original packaging metadata, scripts, and documentation.
