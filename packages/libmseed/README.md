<!-- SPDX-License-Identifier: Apache-2.0 -->
# libmseed

This directory packages EarthScope libmseed 3.5.4 for openEuler 24.03 LTS
SP3 on `riscv64`/RVA23. The official stable tag points to commit
`d6e6ad306de5b7bdde072e5a5e3d58ddcc11abd8`, whose archive is pinned by
SHA-256 and can be retrieved over HTTPS in the target build. The official
`LICENSE` grants Apache-2.0.

The frozen discovery snapshot contained old 2.x Debian/Ubuntu records with
no license metadata. That did not establish the current upstream license;
the official 3.5.4 source resolves it. Its archive has only in-tree symlinks
from `test/` to `example/`, plus bundled reference records.

`%check` runs all 11 registered upstream CTest cases with bundled fixtures.
All examples are compiled, and libcurl URL support is enabled. Installed
smoke links through `pkg-config` and checks a deterministic nanosecond time
conversion. These checks do not prove native RISC-V hardware behavior or
repository publication. The repository's Apache-2.0 license covers original
packaging files only.
