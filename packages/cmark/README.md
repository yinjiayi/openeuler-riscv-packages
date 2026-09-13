<!-- SPDX-License-Identifier: Apache-2.0 -->
# cmark

This directory packages cmark `0.31.2` for openEuler 24.03 LTS SP3 on
`riscv64`/RVA23. The immutable official version-tag archive is independently
SHA-256 pinned and passed single-root, path, link, and special-entry safety
inspection. Arch stable confirms 0.31.2; Fedora 44, openSUSE Tumbleweed,
Debian stable, and Ubuntu 26.04 LTS GA retained older stable releases. This is
therefore an intentional official-stable forward release.

AUR was queried through RPC only. Its matching `cmark-git` row is VCS-only and
was excluded as a source; no PKGBUILD or distribution spec was executed. The
build enables the shared library and the complete upstream CTest suite,
including API, specification, entity, pathological, regression, smart
punctuation, and round-trip tests. Installed smoke exercises both the CLI and
the public libcmark API without network access.

External source licenses remain those of upstream. Apache-2.0 covers only the
original packaging metadata, scripts, tests, and documentation in this repo.
