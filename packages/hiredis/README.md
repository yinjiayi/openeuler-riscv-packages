<!-- SPDX-License-Identifier: Apache-2.0 -->
# hiredis

This directory packages upstream `https://github.com/redis/hiredis` version `1.4.1` for openEuler 24.03 LTS SP3 on `riscv64`/RVA23.

The Fedora 44 `hiredis` dist-git spec (1.2.0) was reviewed as a non-executed packaging reference. This package follows the newer reviewed official 1.4.1 release, keeps the Fedora runtime/devel split, enables the SSL and asynchronous test paths, and runs them against a local Redis server with build-time networking disabled.

External source and patch licenses remain those of their respective upstream projects. The repository license only covers original packaging metadata, scripts, and documentation.
