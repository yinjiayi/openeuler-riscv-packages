<!-- SPDX-License-Identifier: Apache-2.0 -->
# check

This directory packages Check `0.15.2` for openEuler 24.03 LTS SP3 on `riscv64`/RVA23. Fedora 44 was the priority discovery source, while Arch stable, Debian stable, openSUSE Tumbleweed, and Ubuntu GA corroborated the same official stable component. The upstream release archive is pinned by SHA-256.

No Fedora spec or AUR content was executed. Documentation generation and optional Subunit integration are excluded from this base package, while the upstream functional test suite and an installed-library test suite remain mandatory and run without network access.

External source and patch licenses remain those of their respective upstream projects. The repository license only covers original packaging metadata, scripts, and documentation.
