<!-- SPDX-License-Identifier: Apache-2.0 -->
# treefrog-framework

This directory packages upstream `https://github.com/treefrogframework/treefrog-framework` version `2.12.0` for openEuler 24.03 LTS SP3 on `riscv64`/RVA23.

External source and patch licenses remain those of their respective upstream projects. The repository license only covers original packaging metadata, scripts, and documentation.

Packaging release 2 uses TreeFrog's project-specific `configure` interface
with its supported installation-directory options. The preceding exact-head
RVA23 build showed that the generic RPM configure macro supplied unsupported
GNU triplet and dependency-tracking arguments, causing the script to print
usage without generating Makefiles. The build, upstream check target, and
install smoke test remain enabled.
