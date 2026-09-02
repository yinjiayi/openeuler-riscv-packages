<!-- SPDX-License-Identifier: Apache-2.0 -->
# wlr-sunclock

This directory packages upstream `https://github.com/sentriz/wlr-sunclock` version `1.2.1` for openEuler 24.03 LTS SP3 on `riscv64`/RVA23.

Release 2 declares `gtk4-devel`, the build dependency identified by exact-head PR CI run 33671450551 when Meson could not resolve `gtk4`. The package keeps the upstream Meson test suite enabled through `%meson_test`; the fresh exact-head CI run is authoritative for the target build result.

External source and patch licenses remain those of their respective upstream projects. The repository license only covers original packaging metadata, scripts, and documentation.
