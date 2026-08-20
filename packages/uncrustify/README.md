<!-- SPDX-License-Identifier: Apache-2.0 -->
# uncrustify

This directory packages Uncrustify 0.83.0 for openEuler 24.03 LTS SP3 on
`riscv64`/RVA23. The source is the immutable asset attached to upstream's
current stable `uncrustify-0.83.0` release and is pinned by a locally
calculated SHA-256 in `sources.yaml`.

Frozen discovery snapshot `discovery-20260808T165000Z-9a89920c269462cd`
records Arch Extra `0.83.0-1`, Debian stable `0.78.1+dfsg1-1`, Fedora 44
`0.82.0-2.fc44`, openSUSE Tumbleweed `0.82.0-1.5`, and Ubuntu Resolute
`0.78.1+dfsg1-1build1`. The official stable source is newer while retaining
the same package lineage. Distribution metadata was not executed.

`%check` runs all 14 upstream CTest entries, which cover the C, C++, C#,
D, ECMAScript, Java, Objective-C, Pawn, Vala, imported and staging corpora,
source formatting, CLI behavior, and sanity checks. The installed smoke test
formats a C expression with a real configuration and verifies the result.

External source licenses remain upstream's GPL-2.0-only terms. Apache-2.0
covers only this repository's original packaging metadata and scripts.
