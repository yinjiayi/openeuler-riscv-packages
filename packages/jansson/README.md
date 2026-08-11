<!-- SPDX-License-Identifier: Apache-2.0 -->
# jansson

This directory packages Jansson `2.15.1` for openEuler 24.03 LTS SP3 on `riscv64`/RVA23. Fedora 44 was the priority distribution lineage. Arch stable, Debian stable, and Ubuntu 26.04 LTS GA still carried older releases when the metadata was frozen, while openSUSE Tumbleweed and the official upstream stable release had advanced to `2.15.1`. The official GitHub release asset is pinned by SHA-256, so this is an intentional stable forward release rather than a Fedora-version copy.

Arch stable `core` and AUR RPC metadata were recorded. The only selected AUR metadata row was a VCS entry last updated more than 24 months before the snapshot, so it was excluded as a source. No AUR recipe, Fedora spec, or other distribution build script is executed. The build is network-free after source verification and runs the upstream functional test suite plus an installed-library compile-and-run smoke test.

External source licenses remain those of the upstream project. The repository license covers only original packaging metadata, scripts, and documentation.
