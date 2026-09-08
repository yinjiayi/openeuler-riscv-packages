<!-- SPDX-License-Identifier: Apache-2.0 -->
# hiredis

This directory packages upstream `https://github.com/redis/hiredis` version `1.4.1` for openEuler 24.03 LTS SP3 on `riscv64`/RVA23.

The Fedora 44 `hiredis` dist-git spec (1.2.0) was reviewed as a non-executed packaging reference. This package follows the newer reviewed official 1.4.1 release, keeps the Fedora runtime/devel split, enables the SSL and asynchronous test paths, and runs them against a local Redis server with build-time networking disabled.

The package-local `0001-tests-use-riscv-qemu-safe-timeout.patch` retains the complete upstream blocking-timeout and SSL reconnect test. The test blocks Redis for one second; on RISC-V only, its command timeout is raised from 10 ms to 500 ms so the negative timeout assertion remains valid while the subsequent TLS handshake can finish under linux-user QEMU. Upstream v1.4.1, the current upstream master, and Fedora 44 do not carry an equivalent fix. Remove the patch once native RISC-V evidence or an upstream architecture-independent margin makes it unnecessary. No upstream issue or PR was created.

External source and patch licenses remain those of their respective upstream projects. The repository license only covers original packaging metadata, scripts, and documentation.
