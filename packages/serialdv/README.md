<!-- SPDX-License-Identifier: Apache-2.0 -->
# serialdv

This directory packages upstream `https://github.com/f4exb/serialDV` version `1.1.5` for openEuler 24.03 LTS SP3 on `riscv64`/RVA23.

Release `2` uses the archive's exact case-sensitive `serialDV-1.1.5` source
root during `%prep`. Release `3` explicitly configures CMake in the build
directory consumed by the openEuler RPM macros. These packaging-only
corrections do not change the pinned upstream source, build features, or tests.

External source and patch licenses remain those of their respective upstream projects. The repository license only covers original packaging metadata, scripts, and documentation.
