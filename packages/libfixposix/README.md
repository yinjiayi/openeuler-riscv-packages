<!-- SPDX-License-Identifier: Apache-2.0 -->
# libfixposix

This directory packages libfixposix 0.5.1 for openEuler 24.03 LTS SP3 on
`riscv64`/RVA23. The source is the immutable archive for upstream's current
stable `v0.5.1` tag (commit `66bda012a7afb232877e315c91e21d6ddaffbdab`)
and is pinned by a locally calculated SHA-256 in `sources.yaml`.

Frozen discovery snapshot `discovery-20260812T010000Z-b30-libfixposix`
records Arch Extra `0.5.1-2`, Debian stable `1:0.5.1-1`, Fedora 44
`0.4.3-17.fc44`, openSUSE Tumbleweed `0.5.1-1.10`, and Ubuntu Resolute
`1:0.5.1-1build1`. Distribution metadata was used only as lineage evidence;
no distribution recipe was read or executed.

The upstream tag contains Autotools inputs rather than generated configure
output, so `%build` regenerates those files with the target toolchain. `%check`
enables and runs the complete Automake gate: the spawn, select, and concurrent
mkstemp executables plus the build-info Bats test, with its compile-only helper
also built. The installed smoke test compiles a consumer through
`libfixposix.pc`, creates a file with `lfp_mkstemp`, and removes it.

libfixposix is BSL-1.0. Apache-2.0 covers only this repository's original
packaging metadata and scripts.
