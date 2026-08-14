<!-- SPDX-License-Identifier: Apache-2.0 -->
# protobuf-c

This directory packages protobuf-c `1.5.2` for openEuler 24.03 LTS SP3
on `riscv64`/RVA23. The official current stable GitHub release asset is
SHA-256 pinned, single-rooted, free of unsafe archive paths and links, and
contains the BSD-2-Clause license and complete maintained Automake tests.

Arch stable, Fedora 44 GA, Debian, openSUSE Tumbleweed, and Ubuntu provide
frozen cross-distribution lineage. AUR was queried through read-only RPC and
had no matching package; no AUR PKGBUILD or distribution recipe was read or
executed. The package upgrades openEuler's `1.4.1-1`, preserves the
`libprotobuf-c.so.1` ABI, the `protoc-c` compatibility link, and the
`protobuf-c-compiler` capability. It builds against the fixed target's
protobuf `25.1-12`. `%check` keeps the compiler enabled and runs every
upstream test under Valgrind; installed smoke generates C from a real schema
and verifies the public runtime version API without network access.

External source licenses remain those of upstream. Apache-2.0 covers only
the original packaging metadata, scripts, tests, and documentation here.
