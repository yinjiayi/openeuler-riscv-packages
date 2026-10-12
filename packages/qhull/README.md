<!-- SPDX-License-Identifier: Apache-2.0 -->
# qhull

This directory packages qhull `2020.2` (upstream library version `8.0.2`)
for openEuler 24.03 LTS SP3 on `riscv64`/RVA23. The official annotated
`2020.2` tag resolves to commit
`613debeaea72ee66626dace9ba1a2eff11b5d37d`; the immutable commit archive is
SHA-256 pinned, single-rooted, and free of unsafe paths, links, or special
members. It contains the upstream Qhull license and the complete maintained
CMake test suite.

Arch stable, read-only AUR RPC metadata, Debian, Fedora 44 GA, and openSUSE
Tumbleweed provide frozen cross-distribution lineage. No AUR PKGBUILD or
distribution recipe was read or executed. Release `2` deliberately
supersedes the target's `2020.2-1` while preserving the command set, the
main/devel/help split, and all three existing ABI compatibility surfaces:
`libqhull.so.8.0`, `libqhull_p.so.8.0`, and `libqhull_r.so.8.0`.

`%check` builds both shared and static targets and runs all 11 canonical
upstream CTest cases without exclusions, including both qset tests, all
command pipelines, and the three user examples. Installed smoke exercises
the command pipeline, verifies the three SONAME capabilities, and compiles
against the public reentrant C API without network access.

External source licenses remain those of upstream. Apache-2.0 covers only
the original packaging metadata, scripts, tests, and documentation here.
