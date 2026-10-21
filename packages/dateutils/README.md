<!-- SPDX-License-Identifier: Apache-2.0 -->
# dateutils

This directory packages dateutils 0.4.11 for openEuler 24.03 LTS SP3 on
`riscv64`/RVA23. The source is the immutable asset attached to upstream's
current stable `v0.4.11` release and is pinned by a locally calculated
SHA-256 in `sources.yaml`.

Frozen discovery snapshot `discovery-20260808T165000Z-9a89920c269462cd`
records Arch Extra `0.4.11-3`, Debian stable `0.4.11-1`, Fedora 44
`0.4.11-7.fc44`, openSUSE Tumbleweed `0.4.11-1.9`, and Ubuntu Resolute
`0.4.11-2`. Distribution metadata was used only as lineage evidence; no
distribution recipe was read or executed.

`%check` runs the complete upstream Automake gate, including its command-line,
calendar-core, parser, formatter, time-zone-map, and round-trip regressions.
The installed smoke test verifies leap-day addition and date-difference
behavior through the installed commands.

External source licenses remain upstream's BSD-3-Clause terms. Apache-2.0
covers only this repository's original packaging metadata and scripts.
