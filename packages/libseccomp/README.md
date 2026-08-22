<!-- SPDX-License-Identifier: Apache-2.0 -->
# libseccomp

This directory packages upstream `https://github.com/seccomp/libseccomp` version `2.6.1` for openEuler 24.03 LTS SP3 on `riscv64`/RVA23.

The current Fedora 44 dist-git spec for 2.6.1 was reviewed as a non-executed packaging reference. The full upstream `%check` remains enabled, including the Python binding pass. A prior digest-locked QEMU run reached the kernel-filter tests but `seccomp_load` returned `ECANCELED`; because QEMU user mode cannot prove target-kernel filtering semantics, this package remains `needs-native-riscv` until an approved native RVA23 runner is available.

External source and patch licenses remain those of their respective upstream projects. The repository license only covers original packaging metadata, scripts, and documentation.
