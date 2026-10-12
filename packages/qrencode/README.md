<!-- SPDX-License-Identifier: Apache-2.0 -->
# qrencode

This directory packages qrencode `4.1.1` for openEuler 24.03 LTS SP3 on
`riscv64`/RVA23. The official v4.1.1 release resolves to commit
`715e29fd4cd71b6e452ae0f4e36d917b43122ce8`; that immutable commit archive
is SHA-256 pinned, single-rooted, and free of unsafe paths, links, or special
members. It includes the upstream LGPL notice and maintained test programs.

Arch stable, Fedora 44 GA, Debian, openSUSE Tumbleweed, and Ubuntu provide
frozen cross-distribution lineage. AUR was queried through read-only RPC and
had no matching package; no AUR PKGBUILD or distribution recipe was read or
executed. Release `3` deliberately supersedes openEuler's existing
`4.1.1-2`, while preserving `libqrencode.so.4`, `qrencode-libs`, and the
main/devel/help package topology. `%check` enables and runs all 12 canonical
upstream test programs without exclusions. Installed smoke verifies PNG
generation and the public C encoding API without network access.

External source licenses remain those of upstream. Apache-2.0 covers only
the original packaging metadata, scripts, tests, and documentation here.
