<!-- SPDX-License-Identifier: Apache-2.0 -->
# expected-lite

This directory packages the official `nonstd-lite/expected-lite` release
`0.10.0` for openEuler 24.03 LTS SP3 on `riscv64`/RVA23.

The frozen discovery snapshot records the component as
`github.com-martinmoene-expected-lite` with Arch stable and openSUSE
Tumbleweed lineage. The project now publishes from the official
`https://github.com/nonstd-lite/expected-lite` repository; the old component
identifier is retained solely for immutable discovery provenance.

The source is the official HTTPS tag archive
`https://github.com/nonstd-lite/expected-lite/archive/refs/tags/v0.10.0.tar.gz`.
Its independently calculated SHA-256 is
`cfe082e4ffedeeedac47763504102646a39c080599c7c1fe99299d6a1f99af92`.
The archive has one relative top-level directory, no parent traversal, no
absolute paths, and no links. CI may use the network while acquiring this
declared source and while resolving audited build dependencies; the source
checksum remains mandatory.

The RPM installs the upstream header and CMake package metadata. `%check`
runs the upstream CTest suite with the non-standard implementation selected,
and the installed smoke test compiles and runs a small `nonstd::expected`
program. No downstream patches are carried.

External source and patch licenses remain those of their respective upstream
projects. The repository license covers only original packaging metadata,
scripts, and documentation.
