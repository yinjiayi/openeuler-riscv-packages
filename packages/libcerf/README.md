<!-- SPDX-License-Identifier: Apache-2.0 -->
# libcerf

This directory packages upstream
`https://jugit.fz-juelich.de/mlz/libcerf` version `3.7` for openEuler 24.03
LTS SP3 on `riscv64`/RVA23.

The frozen discovery snapshot is the immutable metadata capture identified by
`discovery-20260808T165000Z-9a89920c269462cd`. It cross-checks Arch stable
(`1:3.3-2`), Fedora 44 (`3.3-2.fc44`), openSUSE Tumbleweed (`2.4-3.9`),
Debian stable (`2.4-2`), and Ubuntu Resolute GA (`3.1-3`). The same snapshot
was queried for AUR metadata and contained no `libcerf` component; that
negative result is recorded rather than inventing a lineage row. No
distribution recipe or AUR content was read or executed.

The complete maintained upstream test gate is CTest with both the C and C++
interfaces enabled. Upstream registers the eight maintained `*test.c` sources
once for the C library and once for the C++ library, for exactly 16 numerical
tests. The SPEC asserts that count before running the complete suite without
network access. The source is the immutable archive for the publisher's stable
`v3.7` tag, pinned by SHA-256
`9071fd4c02f5a57b909ad733dd7c8ac321642464365691b181c23d66ac6730f6`;
no distribution source or mirror was substituted. The v3.6 packaging repair
that made `%prep` follow the verified GitLab archive root is retained for v3.7,
whose exact root is
`cerf-v3.7-c22fc842bfc5a8cd34cee2f64cc0c830d6b2729c`.

External source licenses remain those of upstream. The repository's
Apache-2.0 license covers only the original packaging metadata, scripts, and
documentation in this directory.
