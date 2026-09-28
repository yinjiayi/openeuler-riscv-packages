<!-- SPDX-License-Identifier: Apache-2.0 -->
# libcdada

This directory packages libcdada 0.6.4 for openEuler 24.03 LTS SP3 on
`riscv64`/RVA23. The upstream annotated `v0.6.4` tag dereferences to commit
`81d9bcb5ec06fb33f5d5b093f0cd8fbfb06174b1`. The official commit archive is
SHA-256 pinned and was inspected for a single root, safe member paths, regular
files, and three relative in-tree symlinks. Its license is BSD-2-Clause.

Frozen openSUSE Tumbleweed 0.6.4-1.3 metadata is discovery lineage only; no
distribution recipe was read or executed. The package installs the C API for
the C++-backed list, map, queue, set, stack, string, and bitmap structures.

`%check` uses the upstream default Automake test target, including generated
custom-type tests and allocation-failure checks. No tests are removed. The
benchmark is built as upstream's non-installed program but is not part of its
registered test suite. Installed smoke compiles a public C list round trip and
checks the installed code generator.

External source licenses remain upstream's. Apache-2.0 covers only original
packaging metadata, scripts, tests, and documentation in this repository.
