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

On RISC-V, the **non-x86 coroutine fallback** is the upstream path that saves
execution state with `sigsetjmp`, moves to a separately allocated stack with
`alloca`, and resumes with `siglongjmp`. Upstream documents this fallback as
incompatible with stack-protector and stack-checking instrumentation. The SPEC
therefore applies the same fallback-safe flags to both the library and the full
test suite. The installed smoke test compiles and executes a real `go()` stack
switch with those flags rather than checking only a non-coroutine API call.

The target CI build deliberately has network access for source and build
dependency retrieval. The complete upstream `make check` suite remains
enabled. The installed smoke test verifies the RPM, pkg-config metadata, and a
small public API link-and-call path.
