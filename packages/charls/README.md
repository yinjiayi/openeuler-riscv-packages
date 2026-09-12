<!-- SPDX-License-Identifier: Apache-2.0 -->
# charls

This directory packages CharLS `2.4.4` for openEuler 24.03 LTS SP3 on
`riscv64`/RVA23. The immutable official stable tag archive is SHA-256
pinned, single-rooted, and contains no unsafe path, link, or special member.
Upstream licenses the library under BSD-3-Clause.

Frozen snapshot `discovery-20260808T165000Z-9a89920c269462cd` cross-checks
Arch extra, Fedora 44 GA, Debian stable, openSUSE Tumbleweed, and Ubuntu
26.04 LTS GA. Read-only AUR RPC found no exact CharLS package. No AUR or
distribution packaging recipe was read or executed.

Version `2.4.4-1` supersedes openEuler's existing `CharLS-2.4.2-1` while
preserving the `CharLS` and `CharLS-devel` package names, CMake/pkg-config
capabilities, and `libcharls.so.2` ABI. `%check` runs upstream's complete
portable `charlstest -unittest` registration against the full in-archive
image and conformance corpus; the separate AFL driver is not a finite test
suite. Installed smoke compiles and runs the public version API.

External source licenses remain those of upstream. Apache-2.0 covers only
the original packaging metadata, scripts, tests, and documentation here.
