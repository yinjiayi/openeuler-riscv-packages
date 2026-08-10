<!-- SPDX-License-Identifier: Apache-2.0 -->
# brotli

This directory packages Brotli 1.2.0 for openEuler 24.03 LTS SP3 on `riscv64`/RVA23. It builds the shared encoder, decoder, and common libraries plus the CLI, runs upstream round-trip and compatibility tests, and repeats an installed-package round trip in the smoke gate.

The immutable discovery record corroborates the component across Arch stable, AUR metadata, Debian stable, Fedora GA, openSUSE Tumbleweed, and Ubuntu GA. The build consumes only the inspected official stable archive pinned in `sources.yaml`; it does not execute AUR or distribution packaging.

The upstream MIT license governs fetched source. Apache-2.0 covers only this repository's original packaging material.
