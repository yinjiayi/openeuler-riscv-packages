<!-- SPDX-License-Identifier: Apache-2.0 -->
# cglm

This directory packages cglm 0.9.6 for openEuler 24.03 LTS SP3 on
`riscv64`/RVA23. The source is the immutable archive for upstream's current
stable `v0.9.6` tag (commit `144d1e7c29b3b0c6dede7917a0476cc95248559c`)
and is pinned by a locally calculated SHA-256 in `sources.yaml`.

Frozen discovery snapshot `discovery-20260812T010000Z-b30-cglm` records Arch
Extra `0.9.6-1`, Debian stable `0.9.6-1`, openSUSE Tumbleweed `0.9.6-1.4`, and
Ubuntu Resolute `0.9.6-1build1`; Fedora 44 has no cglm source package in the
snapshot. Distribution metadata was used only as lineage evidence; no
distribution recipe was read or executed.

`%check` runs the complete upstream CTest aggregate with `CGLM_USE_TEST=ON`.
That aggregate builds and executes all maintained runner sources for scalar,
vector, matrix, Euler, structure, clamp, and Bezier behavior. The installed
smoke test compiles a consumer through `cglm.pc` and verifies an identity
matrix/vector operation through the shared library.

cglm is MIT. Apache-2.0 covers only this repository's original packaging
metadata and scripts.
