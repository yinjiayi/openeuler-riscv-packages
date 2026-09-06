<!-- SPDX-License-Identifier: Apache-2.0 -->
# simplearchiver

This directory packages upstream `https://github.com/Stephen-Seo/SimpleArchiver` version `3.5.0` for openEuler 24.03 LTS SP3 on `riscv64`/RVA23.

Packaging release 3 selects the verified `SimpleArchiver-3.5.0` archive root, uses an explicit CMake build directory, embeds the deterministic `3.5.0` version string, directly executes both upstream unit-test programs because upstream does not register them with CTest, and explicitly installs the built executable because upstream defines no CMake install rule.

External source and patch licenses remain those of their respective upstream projects. The repository license only covers original packaging metadata, scripts, and documentation.
