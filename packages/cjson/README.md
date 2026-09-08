<!-- SPDX-License-Identifier: Apache-2.0 -->
# cjson

This directory packages cJSON `1.7.19` for openEuler 24.03 LTS SP3 on `riscv64`/RVA23. Fedora 44 supplied the priority component identity at `1.7.18`; Arch stable, openSUSE Tumbleweed, and the official upstream release feed established `1.7.19`, so the resolver selected the newer stable release instead of regressing. The official tag archive is pinned by SHA-256.

No Fedora spec or AUR content was executed. The network-free build retains cJSON's upstream tests and validates the installed shared library and pkg-config metadata.

External source and patch licenses remain those of their respective upstream projects. The repository license only covers original packaging metadata, scripts, and documentation.
