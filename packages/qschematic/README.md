<!-- SPDX-License-Identifier: Apache-2.0 -->
# qschematic

This directory packages upstream `https://github.com/simulton/QSchematic` version `3.0.3` for openEuler 24.03 LTS SP3 on `riscv64`/RVA23.

Packaging release 2 selects the verified, case-sensitive `QSchematic-3.0.3` source archive root during `%prep`.

Packaging release 3 declares the required Qt 6 development files and uses one explicit CMake build directory for configuration, build, installation, and CTest. Static and shared libraries plus the demo remain enabled.

Packaging release 4 allows 90 minutes for the QEMU build. Trusted CI completed compilation and CTest under the previous 60-minute limit, then exhausted that deadline while finalizing the RPMs.

Packaging release 5 pins the official GPDS 1.10.0 archive (tag commit
`347db1a6db47f0b98c27ae0172af2c7746746107`, SHA-256
`c0b86573ebfbc76169a43a4508fecf17f2b1b20d44cdba9adf2265ad3e0547e3`).
CMake consumes the verified, unpacked dependency through its supported
`FETCHCONTENT_SOURCE_DIR_GPDS` setting; no configuration-time Git fetch is needed.
GPDS includes MiniYAML (MIT) and TinyXML-2 (Zlib), whose license notices are
packaged alongside GPDS's MIT notice. The build retains the shared/static
libraries, demo and CTest suite. The 120-minute budget accounts for the observed
slow dependency installation; completion remains subject to CI verification.

External source and patch licenses remain those of their respective upstream projects. The repository license only covers original packaging metadata, scripts, and documentation.
