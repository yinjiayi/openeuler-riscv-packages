<!-- SPDX-License-Identifier: Apache-2.0 -->
# tree

This directory packages tree `2.3.2` for openEuler 24.03 LTS SP3 on
`riscv64`/RVA23. Its immutable official release archive is SHA-256 pinned and
passed archive-safety inspection. Arch stable and openSUSE Tumbleweed confirm
2.3.2; Fedora 44, Debian stable, and Ubuntu 26.04 LTS GA carried older stable
releases, making this an intentional official-stable forward release.

AUR was queried only through metadata RPC. Exact-name and search snapshots had
no matching tree component package; unrelated name matches were rejected and
no PKGBUILD was read or executed. Distribution specs were untrusted, read-only
lineage evidence. Upstream 2.3.2 ships no test target or dedicated test suite;
the SPEC therefore adds a deterministic build-tree functional check rather
than claiming or skipping nonexistent tests. The installed smoke test exercises
text and JSON output with hidden files, and all operations are network-free.

External source licenses remain those of upstream. Apache-2.0 covers only the
original packaging metadata, scripts, tests, and documentation in this repo.
