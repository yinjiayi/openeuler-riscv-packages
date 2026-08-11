<!-- SPDX-License-Identifier: Apache-2.0 -->
# macchanger

This directory packages upstream `https://github.com/alobbs/macchanger` version `1.7.0` for openEuler 24.03 LTS SP3 on `riscv64`/RVA23.

External source and patch licenses remain those of their respective upstream projects. The repository license only covers original packaging metadata, scripts, and documentation.

Fedora 44's official 1.7.0-30.fc44 source package was inspected as
cross-distribution packaging evidence. Its two small correctness patches for
random-source selection, complete seed reads, and portable size_t formatting
are retained locally with provenance; the Fedora SPEC and patches were not
executed.

Functional validation must change and restore a live interface through privileged
networking ioctls, so it remains `needs-native-riscv`; QEMU user mode is only a
compilation boundary for this package.
