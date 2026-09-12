<!-- SPDX-License-Identifier: Apache-2.0 -->
# cppitertools

This directory packages upstream `https://github.com/ryanhaining/cppitertools` version `2.2` for openEuler 24.03 LTS SP3 on `riscv64`/RVA23.

External source and patch licenses remain those of their respective upstream projects. The repository license only covers original packaging metadata, scripts, and documentation.

Release 2 uses the repository's separate CMake build directory, stages the
pinned Catch2 2.13.10 header, and executes upstream's complete `test_all`
aggregate. The installed result is a header-only, architecture-independent RPM.
