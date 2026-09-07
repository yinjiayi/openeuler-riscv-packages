<!-- SPDX-License-Identifier: Apache-2.0 -->
# sniffercommit

This directory packages upstream `https://github.com/slowy07/sniffercommit` version `0.3.3` for openEuler 24.03 LTS SP3 on `riscv64`/RVA23.

GitHub redirects the upstream repository to `https://github.com/slowy07/metis`; consequently, the pinned `v0.3.3` archive has the top-level directory `metis-0.3.3`. The build keeps upstream's real CTest suite enabled and uses its pinned FetchContent dependencies, so `git` is a declared build requirement and build-time network access remains explicit in `package.yaml`.

Release 4 supplies explicit `-S` and `-B` paths because upstream rejects in-source builds. Configure, build, install, and the complete CTest suite all use `%{_vpath_builddir}`. It also declares `clang-tools-extra`, the official openEuler RVA23 provider for `/usr/bin/clang-format`, because `FormatModeTest.DryRunFormat` exercises that executable.

External source and patch licenses remain those of their respective upstream projects. The repository license only covers original packaging metadata, scripts, and documentation.
