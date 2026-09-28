# libigloo 0.9.5

The frozen inventory's exact `libigloo` key maps to the Xiph Icecast project's
[official GitLab source](https://gitlab.xiph.org/xiph/icecast-libigloo).
Its latest stable `v0.9.5` tag resolves to commit
`1a4f57543f3d441982f6999370fd8a23c229b592`. The official HTTPS tag
archive is SHA-256 pinned at
`67a9a1d667033eda06adb1306d3a80e9125246f616d1ffe362395fb2b32aae61`.
All 92 archive members were checked for unsafe paths, links, and device nodes.

The frozen discovery snapshot flagged missing distribution license metadata;
that was not evidence of proprietary licensing. The official `COPYING` and
source/header notices explicitly grant GNU Library GPL version 2 or later,
represented in RPM metadata as `LGPL-2.0-or-later`.

The build needs `rhash-devel`, available in the configured official openEuler
24.03 LTS SP3 RVA23 Everything repository (1.4.4-2.oe2403sp3). `%check`
runs all ten upstream Automake TAP suites. Their TAP driver fails on a reported
`not ok` even for a test program returning zero. Installed smoke independently
compiles an external client using `igloo.pc` and checks the public version API.

The target is openEuler 24.03 LTS SP3, `riscv64`, RVA23. The QEMU-user test
evidence covers API behavior, not the quality of a native hardware entropy
source or timing/performance. PR CI artifacts do not establish public RPM/SRPM
publication; that requires a separate verified repository result.
