<!-- SPDX-License-Identifier: Apache-2.0 -->
# watchflower

This directory packages upstream `https://github.com/emericg/WatchFlower` version `5.4` for openEuler 24.03 LTS SP3 on `riscv64`/RVA23.

Release 3 uses the archive's case-sensitive `WatchFlower-5.4` source root and an explicit out-of-source CMake directory. The build declares the Qt 6 base/private, connectivity, declarative, SVG, and Charts development packages used by the desktop target and its bundled libraries, together with `libxkbcommon-devel`, which provides the XKB interface required by `Qt6::GuiPrivate`. Upstream 5.4 defines no CTest cases; `%check` remains enabled as a test-discovery gate but is not treated as unit-test coverage.

External source and patch licenses remain those of their respective upstream projects. The repository license only covers original packaging metadata, scripts, and documentation.
