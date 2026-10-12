<!-- SPDX-License-Identifier: Apache-2.0 -->
# stressapptest

This directory packages upstream `https://github.com/stressapptest/stressapptest` version `1.0.11` for openEuler 24.03 LTS SP3 on `riscv64`/RVA23.

Fedora 44 currently carries an older 1.0.9 snapshot; its dist-git spec was reviewed as a non-executed packaging reference. This package uses the newer reviewed official 1.0.11 release corroborated by Debian stable, openSUSE Tumbleweed, and Ubuntu GA. Its short stress test remains in `%check`, but the package is routed to `needs-native-riscv`: QEMU user mode cannot validate physical memory, cache-coherency, timing, or I/O-device behavior.

External source and patch licenses remain those of their respective upstream projects. The repository license only covers original packaging metadata, scripts, and documentation.
