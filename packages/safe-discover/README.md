<!-- SPDX-License-Identifier: Apache-2.0 -->
# safe-discover

This directory packages upstream `https://github.com/kinncj/Safe-Discover` version `0.2.1` for openEuler 24.03 LTS SP3 on `riscv64`/RVA23.

External source and patch licenses remain those of their respective upstream projects. The repository license only covers original packaging metadata, scripts, and documentation.

Release 2 binds `%prep` to the case-sensitive `Safe-Discover-0.2.1` root in the checksum-verified upstream tag archive. Trusted pull-request CI confirmed the default lowercase RPM directory name did not exist; tests and installed-package smoke coverage remain enabled.

Release 3 declares `extra-cmake-modules`, the package providing the required `ECMConfig.cmake`. Exact-head trusted CI run `34036308983` reached upstream CMake after the archive-root repair and failed only because this declared configuration dependency was absent; build, test, and smoke behavior remain unchanged.
