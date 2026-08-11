<!-- SPDX-License-Identifier: Apache-2.0 -->
# yajl

This directory packages YAJL `2.1.0` for openEuler 24.03 LTS SP3 on `riscv64`/RVA23. Fedora 44 was the priority discovery source; Arch stable, Debian stable, and openSUSE Tumbleweed corroborated the same official release. The upstream tag archive is pinned by SHA-256.

No external distribution recipe or AUR content was executed. Both upstream parser and API test targets remain mandatory, followed by installed JSON-tool and C API smoke tests, with no build-time network access.

External source and patch licenses remain those of their respective upstream projects. The repository license only covers original packaging metadata, scripts, and documentation.
