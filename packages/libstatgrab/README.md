<!-- SPDX-License-Identifier: Apache-2.0 -->
# libstatgrab

This directory packages the stable `libstatgrab` 0.92.1 release for openEuler
24.03 LTS SP3 on `riscv64`/RVA23. The official GitHub release archive is
pinned by SHA-256 in `sources.yaml`; its 244 members are under one top-level
directory and have no absolute paths, parent traversal, links, or special
files. The archive contains the upstream LGPL-2.1-or-later library license
and GPL-2.0-or-later utility/example license.

The frozen discovery snapshot `discovery-20260808T165000Z-9a89920c269462cd`
records the package in Arch stable, openSUSE Tumbleweed, Fedora 44 GA, Debian
stable, and Ubuntu Resolute GA. AUR metadata identifies only separate Perl
bindings and is not used as source or packaging input. The fixed openEuler
SP3/RVA23 repository and the reviewed supplement have no existing package,
provider, or reverse consumer for `libstatgrab`, `statgrab`, `saidar`, or the
`libstatgrab.so.10` SONAME.

The SPEC enables upstream's required Perl/TAP automation (`--enable-tests=yes`)
and runs the complete `make -j1 check` matrix. The explicit serial order is
required because the generated TAP harness shares output state; it preserves
all single-threaded and multi-threaded function-combination tests without
disabling or converting any case to a skip. The installed smoke test verifies all three runtime packages,
the public header and pkg-config metadata, links a small API consumer, and
checks the utility version.

External source licenses remain those of the upstream project. The repository
license covers only these packaging metadata and smoke-test files.
