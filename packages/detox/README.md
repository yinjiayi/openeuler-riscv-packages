<!-- SPDX-License-Identifier: Apache-2.0 -->
# detox

This directory packages detox 3.0.1 for openEuler 24.03 LTS SP3 on
`riscv64`/RVA23. The immutable source is the official asset attached to
upstream's current stable `v3.0.1` release (tag commit
`7dd831c10f1ed1ec12124ffa231208489ea50041`). Its SHA-256 agrees with the
digest published by the GitHub release API and is pinned in `sources.yaml`.
The archive contains one source root and no unsafe paths, special files, or
escaping links.

Frozen discovery snapshot `discovery-20260812T150000Z-b34-detox` records
Arch Extra `3.0.1-1`, Debian stable `2.0.0-4`, Fedora 44
`3.0.1-3.fc44`, and Ubuntu Resolute `2.0.0-3ubuntu2`; the frozen openSUSE
and AUR catalogs have no matching canonical detox package. Distribution
metadata was used only as lineage evidence; no distribution recipe was read
or executed.

The target repository contains Bash `5.2.15-19.oe2403sp3`, Check-devel
`0.15.2-2.oe2403sp3`, GCC `14.3.1-10.oe2403sp3`, glibc locale archive
`2.38-84.oe2403sp3`, GNU Make `1:4.4.1-2.oe2403sp3`, pkgconf
`1.9.5-2.oe2403sp3`, and Valgrind `1:3.25.1-4.oe2403sp3`; it contains
neither detox nor an `inline-detox` provider.

CI fetches and verifies the pinned source during the network-enabled build.
`%check` enables Check explicitly and runs the full maintained upstream
suite. The fail-closed legacy driver runs all 17 issue/directory/man-page
scenarios and the Check harness runs all 14 unit executables. Exact-head run
`31761326115` showed that the repository's Valgrind cannot start against the
stripped RISC-V dynamic loader because compatible glibc debuginfo is outside
the approved build-dependency repository. A downstream test-only patch probes
the exact detox binary, skips instrumentation only for the two known startup
signatures, and leaves every other Valgrind failure fatal; the issue 56
functional stress loop still runs. The installed smoke verifies the version,
renames an actual file, and checks the deterministic `inline-detox` stream
transformation. Fresh exact-head CI remains the target authority.

detox is BSD-3-Clause. Apache-2.0 covers only this repository's original
packaging metadata and scripts.
