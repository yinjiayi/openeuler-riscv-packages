<!-- SPDX-License-Identifier: Apache-2.0 -->
# libmnl

This directory packages libmnl `1.0.5` for openEuler 24.03 LTS SP3 on `riscv64`/RVA23. Fedora 44 was the priority discovery source; Arch stable, Debian stable, openSUSE Tumbleweed, and Ubuntu GA corroborated the same stable component. The official Netfilter archive is pinned by SHA-256.

No external distribution recipe or AUR content was executed. Upstream checks remain enabled, and the installed smoke test exercises in-memory Netlink message construction without requiring privileges or a live Netlink transaction.

External source and patch licenses remain those of their respective upstream projects. The repository license only covers original packaging metadata, scripts, and documentation.
