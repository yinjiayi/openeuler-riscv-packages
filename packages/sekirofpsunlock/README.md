<!-- SPDX-License-Identifier: Apache-2.0 -->
# sekirofpsunlock

This directory packages upstream `https://github.com/Lahvuun/sekirofpsunlock` version `0.2.3` for openEuler 24.03 LTS SP3 on `riscv64`/RVA23.

Packaging release 2 explicitly installs the executable because upstream defines no Meson install rule. The pinned archive has no upstream test definitions, so the packaging retains Meson test discovery without manufacturing a game or ptrace integration test.

External source and patch licenses remain those of their respective upstream projects. The repository license only covers original packaging metadata, scripts, and documentation.
