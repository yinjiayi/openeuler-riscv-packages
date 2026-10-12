<!-- SPDX-License-Identifier: Apache-2.0 -->
# libuev

This directory packages upstream `https://github.com/troglobit/libuev`
version `2.4.1` for openEuler 24.03 LTS SP3 on `riscv64`/RVA23.

The frozen discovery snapshot is the immutable metadata capture identified by
`discovery-20260808T165000Z-9a89920c269462cd`. It cross-checks AUR
(`2.4.1-2`), Fedora 44 (`2.4.1-5.fc44`), openSUSE Tumbleweed (`2.4.1-2.9`),
Debian stable (`2.4.1-1`), and Ubuntu Resolute GA (`2.4.1-1build2`). The same
snapshot was queried for Arch stable metadata and contained no `libuev`
component; that negative result is recorded rather than inventing a lineage
row. No distribution recipe or AUR content was read or executed.

The complete maintained upstream test gate is `make check`. It runs all seven
active, API, completion, cron, signal, timer, and event-loop tests without
network access. The archive and its SHA-256 sidecar are publisher release
assets; no distribution source or mirror was substituted.

External source licenses remain those of upstream. The repository's
Apache-2.0 license covers only the original packaging metadata, scripts, and
documentation in this directory.
