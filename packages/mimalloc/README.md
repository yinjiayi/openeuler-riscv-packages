<!-- SPDX-License-Identifier: Apache-2.0 -->
# mimalloc

This directory packages upstream `mimalloc` 3.5.2 for openEuler 24.03 LTS SP3 on `riscv64`/RVA23. The official stable GitHub tag archive is pinned by SHA-256 in `sources.yaml`; distribution records are discovery lineage only. The complete upstream CTest suite registered by the portable build remains enabled. Installed smoke verifies the upstream `3.5` pkg-config compatibility line and the exact `30502` header/runtime version before exercising allocation and release through the public API; it is functional evidence, not a native performance benchmark.

The upstream MIT license governs the fetched source. Apache-2.0 covers only this repository's original packaging material. Reviewed-registry enrichment for this release is tracked separately and is not part of this package-only change.
