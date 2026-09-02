<!-- SPDX-License-Identifier: Apache-2.0 -->
# wlr-sunclock

This directory packages upstream `https://github.com/sentriz/wlr-sunclock` version `1.2.1` for openEuler 24.03 LTS SP3 on `riscv64`/RVA23.

Release 2 declares `gtk4-devel`, the build dependency identified by exact-head PR CI run 33671450551 when Meson could not resolve `gtk4`. The package keeps the upstream Meson test suite enabled through `%meson_test`; the fresh exact-head CI run is authoritative for the target build result.

Exact-head Package CI run `33673093171` for commit
`9682858722a4178abf4d9a338b0c56fe66d2e594` resolved GTK 4 and then stopped at
the next effective Meson error: `gtk4-layer-shell-0` was unavailable. Release 3
declares `pkgconfig(gtk4-layer-shell-0)`. The managed provider
`gtk4-layer-shell` 1.3.0-5 has passed exact-head PR CI, but it has no published
repository URL while the quarantined self-hosted runner fleet remains offline;
therefore this package is dependency-blocked rather than claimed buildable.

External source and patch licenses remain those of their respective upstream projects. The repository license only covers original packaging metadata, scripts, and documentation.
