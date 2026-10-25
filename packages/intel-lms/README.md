<!-- SPDX-License-Identifier: Apache-2.0 -->
# intel-lms

This directory packages upstream `https://github.com/intel/lms` version `2625.0.0.0` for openEuler 24.03 LTS SP3 on `riscv64`/RVA23.

The pinned official tag archive extracts to `lms-2625.0.0.0`, rather than the RPM name-derived `intel-lms-2625.0.0.0`. The SPEC passes that verified archive root explicitly to `%autosetup`; it does not rename or repack the upstream source.

External source and patch licenses remain those of their respective upstream projects. The repository license only covers original packaging metadata, scripts, and documentation.
