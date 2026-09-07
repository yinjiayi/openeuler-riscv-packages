<!-- SPDX-License-Identifier: Apache-2.0 -->
# sniffercommit

This directory packages upstream `https://github.com/slowy07/sniffercommit` version `0.3.3` for openEuler 24.03 LTS SP3 on `riscv64`/RVA23.

GitHub redirects the upstream repository to `https://github.com/slowy07/metis`; consequently, the pinned `v0.3.3` archive has the top-level directory `metis-0.3.3`. The build keeps upstream's real CTest suite enabled and uses its pinned FetchContent dependencies, so `git` is a declared build requirement and build-time network access remains explicit in `package.yaml`.

External source and patch licenses remain those of their respective upstream projects. The repository license only covers original packaging metadata, scripts, and documentation.
