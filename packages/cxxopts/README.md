<!-- SPDX-License-Identifier: Apache-2.0 -->
# cxxopts

This directory packages cxxopts 3.3.1 for openEuler 24.03 LTS SP3 on
`riscv64`/RVA23. The source is the immutable archive for upstream's current
stable `v3.3.1` tag (commit `44380e5a44706ab7347f400698c703eb2a196202`)
and is pinned by a locally calculated SHA-256 in `sources.yaml`.

Frozen discovery snapshot `discovery-20260808T165000Z-9a89920c269462cd`
records Arch Extra `3.3.1-1`, Debian stable `3.2.1-1`, Fedora 44
`3.3.1-4.fc44`, openSUSE Tumbleweed `3.3.1-1.4`, and Ubuntu Resolute
`3.3.1-1`. Distribution metadata was used only as lineage evidence; no
distribution recipe was read or executed.

`%check` runs all three registered upstream CTest cases: the option parser,
installed-package discovery, and add-subdirectory integration. The build also
compiles upstream examples and link tests. The installed smoke test compiles a
consumer with the installed header and validates real option parsing.

The installed cxxopts header is MIT. The source archive's maintained tests
vendor Catch under BSL-1.0, so both licenses are declared. Apache-2.0 covers
only this repository's original packaging metadata and scripts.
