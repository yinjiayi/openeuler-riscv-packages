<!-- SPDX-License-Identifier: Apache-2.0 -->
# xz

This directory packages XZ Utils `5.8.3` for openEuler 24.03 LTS SP3 on
`riscv64`/RVA23. The official stable release is newer than the Fedora 44
`1:5.8.2-2.fc44` and Debian stable `5.8.1-1+deb13u1` snapshots, while Arch
stable, openSUSE Tumbleweed, and Ubuntu 26.04 LTS GA had already moved to the
5.8.3 release line. Fedora's downstream Epoch is recorded as lineage evidence
but is intentionally not copied onto the epoch-less openEuler package.

The immutable official release asset is pinned by SHA-256 and passed an
archive inspection for a single expected root, safe paths and links, and no
special entries. Arch stable and AUR RPC metadata were frozen; the selected
AUR row is metadata only. No AUR recipe was read or executed; Fedora and
openSUSE specs were reviewed only as untrusted, read-only lineage evidence and
were never executed. The network-free build runs the complete upstream
test suite, and the installed smoke test exercises both command-line
round-trips and the public liblzma API.

External source licenses remain those of the upstream project. The repository
license covers only original packaging metadata, scripts, and documentation.
