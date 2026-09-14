<!-- SPDX-License-Identifier: Apache-2.0 -->
# libcerf

This directory packages upstream
`https://jugit.fz-juelich.de/mlz/libcerf` version `3.6` for openEuler 24.03
LTS SP3 on `riscv64`/RVA23.

The frozen discovery snapshot is the immutable metadata capture identified by
`discovery-20260808T165000Z-9a89920c269462cd`. It cross-checks Arch stable
(`1:3.3-2`), Fedora 44 (`3.3-2.fc44`), openSUSE Tumbleweed (`2.4-3.9`),
Debian stable (`2.4-2`), and Ubuntu Resolute GA (`3.1-3`). The same snapshot
was queried for AUR metadata and contained no `libcerf` component; that
negative result is recorded rather than inventing a lineage row. No
distribution recipe or AUR content was read or executed.

The complete maintained upstream test gate is CTest with both the C and C++
interfaces enabled. It runs all 18 registered numerical tests without network
access. The source is the immutable archive for the publisher's current stable
`v3.6` tag; no distribution source or mirror was substituted. Exact-head run
`33227448843` attempt 2 verified that archive and exposed the stale v3.3 commit
root in `%prep`; the current SPEC follows the archive's versioned root.

External source licenses remain those of upstream. The repository's
Apache-2.0 license covers only the original packaging metadata, scripts, and
documentation in this directory.
