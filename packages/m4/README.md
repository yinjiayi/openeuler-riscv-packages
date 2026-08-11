<!-- SPDX-License-Identifier: Apache-2.0 -->
# m4

This directory packages GNU M4 `1.4.21` for openEuler 24.03 LTS SP3 on `riscv64`/RVA23. Fedora 44 was the priority discovery source; Arch stable, Debian stable, and openSUSE Tumbleweed corroborated the same official stable release. The GNU release archive is pinned by SHA-256.

No external distribution recipe or AUR content was executed. The complete upstream test suite remains mandatory and is run serially, followed by an installed macro-expansion smoke test, with no build-time network access.

External source and patch licenses remain those of their respective upstream projects. The repository license only covers original packaging metadata, scripts, and documentation.
