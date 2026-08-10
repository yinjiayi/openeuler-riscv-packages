<!-- SPDX-License-Identifier: Apache-2.0 -->
# aml

This directory packages upstream aml 1.0.0 for openEuler 24.03 LTS SP3 on `riscv64`/RVA23. The Meson build produces the shared event-loop library and development files; `%check` executes the upstream reader example through its epoll loop.

The immutable discovery record corroborates the component across Arch stable, AUR metadata, Debian stable, Fedora GA, openSUSE Tumbleweed, and Ubuntu GA. The source is the inspected official upstream release archive pinned in `sources.yaml`; no AUR or distribution packaging instructions are executed.

The upstream ISC license governs fetched source. Apache-2.0 covers only this repository's original packaging material.
