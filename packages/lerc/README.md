<!-- SPDX-License-Identifier: Apache-2.0 -->
# lerc

This directory packages Lerc 4.2.0 for openEuler 24.03 LTS SP3 on
`riscv64`/RVA23. The immutable source is upstream's current stable `v4.2.0`
tag (commit `e534980e11992cc5f11864b0dcff1af6a27cee0d`) and is pinned by the
locally calculated SHA-256 in `sources.yaml`.

Frozen discovery snapshot `discovery-20260812T010000Z-b30-lerc` records AUR
`4.1.1-1`, Debian stable `4.0.0+ds-5`, Fedora 44 source package `liblerc`
`4.0.0-10.fc44`, openSUSE Tumbleweed `4.1.0-3.3`, and Ubuntu Resolute
`4.0.0+ds-5ubuntu2`. Distribution metadata was used only as lineage evidence;
no distribution recipe was read or executed.

`%check` compiles and runs the complete maintained upstream `LercTest` program.
It exercises lossless and lossy encode/decode, masks, multi-band data, NaNs,
and the 4-D no-data API, and must finish with `SUMMARY: all good`. The installed
smoke test compiles a C consumer through `Lerc.pc` and verifies an actual
float encode/decode round trip.

Lerc is Apache-2.0. Apache-2.0 also covers this repository's original
packaging metadata and scripts.
