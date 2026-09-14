<!-- SPDX-License-Identifier: Apache-2.0 -->
# unshield

This directory packages upstream `https://github.com/twogood/unshield` version `1.6.2` for openEuler 24.03 LTS SP3 on `riscv64`/RVA23.

Packaging release 3 declares the required Zlib development dependency, uses explicit CMake source and build directories, and lists the manual page separately with a compression-aware RPM file glob. This matches the `brp-compress` transformation observed in exact-head run `34029101040` without weakening the package contents. The pinned upstream archive has no test directory, so the packaging does not manufacture test cases.

External source and patch licenses remain those of their respective upstream projects. The repository license only covers original packaging metadata, scripts, and documentation.
