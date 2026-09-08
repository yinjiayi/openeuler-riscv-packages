<!-- SPDX-License-Identifier: Apache-2.0 -->
# libidn

This directory packages GNU Libidn `1.44` for openEuler 24.03 LTS SP3 on
`riscv64`/RVA23. The immutable GNU release archive is SHA-256 pinned and
passed archive-safety inspection. Arch stable and openSUSE Tumbleweed confirm
1.44, while Fedora 44 stable, Debian stable, and Ubuntu 26.04 LTS GA retained
1.43. This is an intentional official-stable forward release.

AUR was queried through RPC only. Its matching `libidn-git` metadata is both
VCS-only and older than 730 days, so it was excluded as a source; no PKGBUILD
was read or executed. Distribution specs were untrusted, read-only lineage
evidence. Optional Java, C#, Emacs, and valgrind integrations are disabled to
keep this package within the qemu-user boundary; all enabled C library, CLI,
fuzz-regression, and documentation checks from the upstream `make check`
target remain intact. Installed smoke covers IDNA conversion and the public C
API, with no network access.

External source licenses remain those of upstream. Apache-2.0 covers only the
original packaging metadata, scripts, tests, and documentation in this repo.
