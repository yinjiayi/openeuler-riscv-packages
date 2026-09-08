<!-- SPDX-License-Identifier: Apache-2.0 -->
# zopfli

This directory packages upstream `https://github.com/google/zopfli` version
`1.0.3` for openEuler 24.03 LTS SP3 on `riscv64`/RVA23. The latest stable
release tag resolves to immutable commit
`bd64b2f0553d4f1ef4e6627647c5d9fc8c71ffc0`; the source manifest pins that
commit archive rather than relying on a moving branch.

The frozen discovery snapshot is the immutable metadata capture identified by
`discovery-20260808T165000Z-9a89920c269462cd`. It cross-checks Arch stable
`extra` (`1.0.3-5`), Fedora 44 (`1.0.3-15.fc44`), openSUSE Tumbleweed
(`1.0.3-2.11`), Debian stable (`1.0.3-3`), and Ubuntu Resolute GA
(`1.0.3-3build1`). The same snapshot was queried for AUR metadata and contained
no canonical `zopfli` component. No distribution recipe or AUR content was
read or executed.

The complete release-archive test gate runs both official Go/CGO packages:
`go/zopfli` checks deterministic gzip compression, decompression, empty input,
random input, and size bounds; `go/zopflipng` checks lossless PNG optimization
using the shipped fixture. Both passed from a clean source tree in a
network-isolated native `riscv64` environment. The installed surface remains
the target repository's canonical `zopfli` and `zopflipng` tools; temporary
test libraries are not added as a new target ABI.

External source licenses remain those of upstream. The repository's
Apache-2.0 license covers only the original packaging metadata, scripts, and
documentation in this directory.
