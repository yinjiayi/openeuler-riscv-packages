<!-- SPDX-License-Identifier: Apache-2.0 -->
# liblqr

This directory packages the official liblqr 0.4.3 stable release for
openEuler 24.03 LTS SP3 on `riscv64`/RVA23. The upstream download page
identifies 0.4.3 as the latest stable version. Its GitHub `v0.4.3` tag
resolves to commit `704a3194a9a0df7aaddbfa40306583b23407a88b`.
The HTTPS tag archive is pinned to SHA-256
`64b0c4ac76d39cca79501b3f53544af3fc5f72b536ac0f28d2928319bfab6def`.
Its 233 entries form one safe root with no links or duplicate paths.

The frozen inventory identifies `liblqr` as discovered but not managed.
Arch Extra 0.4.3-1 is a live independent lineage cross-check; its recipe was
not executed. Library sources and headers specify LGPL-3.0-only. The
unbuilt example programs have GPL-3.0-only notices and are not packaged.

Upstream does not register a test suite. `%check` and installed-RPM smoke
compile a public-API client, shrink an 8×8 RGB image to 7×8, and assert the
reported dimensions. This tests a representative code path, not the full
seam-carving algorithm or image quality. No privileged devices are needed.

External source remains under its upstream licenses. Apache-2.0 covers only
the original packaging metadata, script, and documentation here.
