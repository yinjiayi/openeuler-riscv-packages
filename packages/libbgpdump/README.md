<!-- SPDX-License-Identifier: Apache-2.0 -->
# libbgpdump

This directory packages RIPE NCC libbgpdump 1.6.2 for openEuler 24.03 LTS
SP3 on `riscv64`/RVA23. The official stable tag resolves to immutable commit
`63fe1c50c7d07bb4c57d4fcc690696adc9b3c306`. Its HTTPS commit archive
is pinned by SHA-256. The smaller release asset omits the upstream regression
fixtures, so the package uses the official tag archive instead.

The upstream `COPYING` and source headers contain HPND-style permission terms
and disclose portions derived from GNU Zebra under GPL-2.0-or-later; the
metadata preserves both. The repository's Apache-2.0 license covers the
original packaging files only.

`%check` executes all 13 bundled MRT fixture comparisons twice: the default
reader output and the optional unknown-attribute (`-u`) output. Installed
smoke runs the upstream CLI's internal `-T` checks and compiles and links a
program against the packaged public API. These tests do not by themselves
prove native RISC-V hardware behavior or repository publication.
