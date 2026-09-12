<!-- SPDX-License-Identifier: Apache-2.0 -->
# libassert

This directory packages upstream `https://github.com/jeremy-rifkin/libassert` version `2.2.1` for openEuler 24.03 LTS SP3 on `riscv64`/RVA23.

The build uses out-of-source CMake configuration and runs the complete registered upstream test suite. The exact cpptrace, magic_enum, googletest, Catch2, and fmt revisions selected by upstream are separate SHA-256-pinned sources. cpptrace uses its addr2line symbol backend, so no untracked libdwarf or zstd source is fetched during configuration.

External source and patch licenses remain those of their respective upstream projects. The repository license only covers original packaging metadata, scripts, and documentation.
