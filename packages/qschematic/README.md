<!-- SPDX-License-Identifier: Apache-2.0 -->
# qschematic

This directory packages upstream `https://github.com/simulton/QSchematic` version `3.0.3` for openEuler 24.03 LTS SP3 on `riscv64`/RVA23.

Packaging release 2 selects the verified, case-sensitive `QSchematic-3.0.3` source archive root during `%prep`.

Packaging release 3 declares the required Qt 6 development files and uses one explicit CMake build directory for configuration, build, installation, and CTest. Static and shared libraries plus the demo remain enabled.

Packaging release 4 allows 90 minutes for the QEMU build. Trusted CI completed compilation and CTest under the previous 60-minute limit, then exhausted that deadline while finalizing the RPMs.

External source and patch licenses remain those of their respective upstream projects. The repository license only covers original packaging metadata, scripts, and documentation.
