<!-- SPDX-License-Identifier: Apache-2.0 -->
# ioping

This directory packages ioping 1.3 for openEuler 24.03 LTS SP3 on
`riscv64`/RVA23. The immutable source is upstream's current stable `v1.3`
tag (commit `d52efa35e1d6d02495434e9447ee04c21b2e1010`) and is pinned by the
locally calculated SHA-256 in `sources.yaml`. The archive contains one source
root and no unsafe paths, special files, or escaping links.

Frozen discovery snapshot `discovery-20260812T140000Z-b34-ioping` records
Arch `1.3-2`, Debian stable `1.3-1`, Fedora 44 `1.3-10.fc44`, openSUSE
Tumbleweed `1.3-1.12`, and Ubuntu Resolute `1.3-1build1`. Distribution
metadata was used only as lineage evidence; no distribution recipe was read
or executed.

The target repository snapshot contains GCC `14.3.1-10.oe2403sp3` and GNU
Make `1:4.4.1-2.oe2403sp3`, and contains no ioping package or provider.
`%check` runs all three commands in upstream's maintained `make test` target:
latency, rapid-read, and request-rate modes perform real temporary filesystem
I/O and all must succeed. The installed smoke independently generates three
I/O requests and checks the request-generation summary.

ioping is GPL-3.0-or-later. Apache-2.0 covers only this repository's original
packaging metadata and scripts.
