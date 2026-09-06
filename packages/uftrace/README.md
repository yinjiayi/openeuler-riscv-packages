<!-- SPDX-License-Identifier: Apache-2.0 -->
# uftrace

This directory packages upstream `https://github.com/namhyung/uftrace` version `0.19` for openEuler 24.03 LTS SP3 on `riscv64`/RVA23.

External source and patch licenses remain those of their respective upstream projects. The repository license only covers original packaging metadata, scripts, and documentation.

Release 2 backports upstream commit `498d3c6cb974f778dea76c27eb770a4821e1a5da`, which fixes the raw ELF comment iterator's accidental one-argument `strcmp` call. The trusted `riscv64` build for pull request 1844 reached this compiler error after dependency installation succeeded; the upstream one-line correction restores the intended `strlen` offset calculation without weakening `%check` or runtime coverage.
