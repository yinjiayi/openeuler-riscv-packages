<!-- SPDX-License-Identifier: Apache-2.0 -->
# sparsehash

This directory packages sparsehash 2.0.4 for openEuler 24.03 LTS SP3 on `riscv64`/RVA23. Although the public API is header-only, configure generates a target-specific internal configuration header, so the RPM remains architecture-specific. The full upstream hash-table test suite runs in `%check`.

The immutable discovery record corroborates the component across Arch stable, AUR metadata, Debian stable, Fedora GA, openSUSE Tumbleweed, and Ubuntu GA. The prefixed official tag is resolved by reviewed metadata, and no AUR content is executed.

The upstream BSD-3-Clause license governs fetched source. Apache-2.0 covers only this repository's original packaging material.
