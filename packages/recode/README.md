<!-- SPDX-License-Identifier: Apache-2.0 -->
# recode

This directory packages Recode `3.7.17` for openEuler 24.03 LTS SP3 on
`riscv64`/RVA23. The official upstream release asset is SHA-256 pinned,
single-rooted, and free of unsafe paths, links, or special archive members.
The archive carries the upstream GPL, LGPL, BSD, and manual-documentation
license texts and includes the complete maintained regression suite.

Arch stable, Fedora 44 GA, Debian, openSUSE Tumbleweed, and Ubuntu provide
frozen cross-distribution lineage. AUR was queried through read-only RPC and
had no matching package; no AUR PKGBUILD or distribution recipe was read or
executed. Version `3.7.17-2` supersedes openEuler's existing `3.7.14-1` while
preserving `librecode.so.3`, the main/devel/help package topology, and the
`recode-static` development capability. `%check` runs the complete canonical
13-file Python/Cython regression suite without a limit or exclusion. Installed
smoke verifies a real character-set conversion and the public C library API
without network access.

Each ordinary main/devel/help subpackage installs `COPYING`, `COPYING-LIB`,
and the complete original `src/ansellat1.l`, `src/iso5426lat1.l`, and
`src/merged.c` through `%license`. These source files retain the upstream BSD
copyright, conditions, and disclaimer without extracting or shortening them;
`merged.c` also retains its original LGPL grants and is not relabeled as BSD-only.
Installed smoke requires exactly one package-owned license file for each of
the five names per subpackage and checks all 15 whole-file SHA-256 values.
These checks require fresh matching-head CI and binary artifacts before
the repaired package can be accepted; previous-head CI is not that evidence.

External source licenses remain those of upstream. Apache-2.0 covers only
the original packaging metadata, scripts, tests, and documentation here.
