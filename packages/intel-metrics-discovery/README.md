<!-- SPDX-License-Identifier: Apache-2.0 -->
# intel-metrics-discovery

This directory packages upstream `https://github.com/intel/metrics-discovery` version `1.14.186` for openEuler 24.03 LTS SP3 on `riscv64`/RVA23.

External source and patch licenses remain those of their respective upstream projects. The repository license only covers original packaging metadata, scripts, and documentation.

Release 6 raises the complete build budget from 120 to 180 minutes. Release 5
reached the final `libigdmd.so` link with link-time optimization (LTO), then
exhausted its remaining 6,614-second rpmbuild budget. The observed compiler
note about variable tracking is a fallback notice, not a compilation failure.
This bounded retry retains LTO, debug information, hardening, the RISC-V patch,
and `%check`; completion still requires a successful target CI run.
