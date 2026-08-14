<!-- SPDX-License-Identifier: Apache-2.0 -->
# libdill

This directory packages the official `libdill` 2.14 tag for openEuler 24.03
LTS SP3 on `riscv64`/RVA23. The GitHub tag archive is pinned by its full
SHA-256 digest in `sources.yaml`.

`libdill` provides structured concurrency, coroutines, channels, and socket
helpers in C. The release archive omits generated Autotools files, so the SPEC
regenerates them after writing the release version marker. The upstream MIT
license governs the fetched source; Apache-2.0 covers this repository's
original packaging files. AUR metadata is retained as lineage only and its
recipe was not executed.

The target CI build deliberately has network access for source and build
dependency retrieval. The complete upstream `make check` suite remains
enabled. The installed smoke test verifies the RPM, pkg-config metadata, and a
small public API link-and-call path.
