<!-- SPDX-License-Identifier: Apache-2.0 -->
# sniffercommit

This directory packages upstream `https://github.com/slowy07/sniffercommit` version `0.3.3` for openEuler 24.03 LTS SP3 on `riscv64`/RVA23.

GitHub redirects the upstream repository to `https://github.com/slowy07/metis`; consequently, the pinned `v0.3.3` archive has the top-level directory `metis-0.3.3`. The build keeps upstream's real CTest suite enabled. Build-time network access remains explicit in `package.yaml` for retrieving declared, SHA-256-verified archives; CMake dependency downloads are disabled.

Release 4 supplies explicit `-S` and `-B` paths because upstream rejects in-source builds. Configure, build, install, and the complete CTest suite all use `%{_vpath_builddir}`. It also declares `clang-tools-extra`, the official openEuler RVA23 provider for `/usr/bin/clang-format`, because `FormatModeTest.DryRunFormat` exercises that executable.

Release 5 declares the official fmt 11.0.2, tomlplusplus 3.4.0 and GoogleTest 1.15.2 archives in `sources.yaml`, pins each SHA-256, and supplies their extracted directories through `FETCHCONTENT_SOURCE_DIR_*` with `FETCHCONTENT_FULLY_DISCONNECTED=ON`. The dependencies are private static/header-only build inputs: fmt and GoogleTest installation is disabled, while upstream tomlplusplus installs only when built as its top-level project. The application does not install third-party library, CMake or pkg-config providers. All 23 upstream tests remain enabled; the unchanged installed smoke checks RPM installation, not CLI functional behavior.

The MIT notices for fmt and tomlplusplus and BSD-3-Clause notice for GoogleTest are included as distinct license files. Source archives are checksum-pinned official tag snapshots, not signature-authenticated release attestations.

External source and patch licenses remain those of their respective upstream projects. The repository license only covers original packaging metadata, scripts, and documentation.
