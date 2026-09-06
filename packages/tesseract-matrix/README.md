<!-- SPDX-License-Identifier: Apache-2.0 -->
# tesseract-matrix

This directory packages upstream `https://github.com/surakin/tesseract` version `0.8.16` for openEuler 24.03 LTS SP3 on `riscv64`/RVA23.

External source and patch licenses remain those of their respective upstream projects. The repository license only covers original packaging metadata, scripts, and documentation.

The downstream CMake patch resolves the target link-feature conflict reported
by CMake 3.27 when the mutually dependent client, SDK bridge, and Rust archives
reach the Qt executable and complete test executable through both ordinary and
`WHOLE_ARCHIVE` links. It keeps whole-archive symbol retention and the complete
test target enabled, and can be removed when upstream carries an equivalent
link-graph fix.
