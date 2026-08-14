<!-- SPDX-License-Identifier: Apache-2.0 -->
# variant-lite

This directory packages the official `nonstd-lite/variant-lite` release
`3.0.0` for openEuler 24.03 LTS SP3 on `riscv64`/RVA23.

The frozen discovery snapshot records the component as
`github.com-martinmoene-variant-lite` with Fedora lineage. The project now
publishes from the official `https://github.com/nonstd-lite/variant-lite`
repository; the old component identifier is retained solely for immutable
discovery provenance.

The source is the official HTTPS tag archive
`https://github.com/nonstd-lite/variant-lite/archive/refs/tags/v3.0.0.tar.gz`.
Its independently calculated SHA-256 is
`bd596550369f33ef9455566822f5a4d52852a63a33d3d70ac1fbb529b78abc7b`.
The archive has one relative top-level directory, no parent traversal, no
absolute paths, and no links. CI may use the network while acquiring this
declared source and while resolving audited build dependencies; the source
checksum remains mandatory.

The RPM installs the upstream header and CMake package metadata. `%check`
runs the upstream CTest suite with the non-standard implementation selected,
and the installed smoke test compiles and runs a small `nonstd::variant`
program. No downstream patches are carried.

External source and patch licenses remain those of their respective upstream
projects. The repository license covers only original packaging metadata,
scripts, and documentation.
