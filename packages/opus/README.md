<!-- SPDX-License-Identifier: Apache-2.0 -->
# opus

This directory packages Opus `1.6.1` for openEuler 24.03 LTS SP3 on
`riscv64`/RVA23. The official current stable release is newer than Fedora
44's 1.6 line and Debian stable's 1.5.2 line, while Arch stable, openSUSE
Tumbleweed, and Ubuntu 26.04 LTS GA had already moved to 1.6.1.

The official Xiph release page publishes the same SHA-256 pinned here. The
archive passed inspection for a single expected root, safe paths and links,
and no special entries. Arch stable and AUR RPC metadata were frozen; no AUR
recipe was read or executed. Distribution specs were reviewed only as
untrusted, read-only lineage evidence and were never executed. The build is
network-free, preserves custom-mode and hardening support, and runs the
complete upstream test suite. The installed smoke test performs an actual
encode/decode round-trip through the public Opus API.

External source licenses remain those of the upstream project. The repository
license covers only original packaging metadata, scripts, and documentation.
