<!-- SPDX-License-Identifier: Apache-2.0 -->
# libplist

This directory packages the official libplist 2.7.0 stable release for
openEuler 24.03 LTS SP3 on `riscv64`/RVA23. The release page is
`https://github.com/libimobiledevice/libplist/releases/tag/2.7.0`.
Its HTTPS source asset is pinned to SHA-256
`7ac42301e896b1ebe3c654634780c82baa7cb70df8554e683ff89f7c2643eb8b`.
The archive has 225 members under one root, all regular files or directories,
with no duplicate names or unsafe paths.

The frozen discovery snapshot contains exact `libplist` lineage from Arch
Extra 2.7.0, Debian 2.6.0, Fedora 44 2.6.0, openSUSE Tumbleweed 2.6.0, and
Ubuntu 26.04 2.7.0. These distribution rows are independent cross-checks,
not source checksums or build instructions. No distribution recipe was run.

Upstream source headers grant LGPL-2.1-or-later for the library and utility;
the bundled `jsmn` and `time64` sources carry MIT notices. `%check` retains
the complete upstream format test suite, including XML, binary, JSON, and
OpenStep cases. Installed-RPM smoke performs a JSON-to-binary-to-JSON
round trip and compiles and runs a program against the public C API.

The optional Cython Python bindings are outside this C/C++ package and are
not built. External source remains under its upstream licenses; Apache-2.0
covers only the original packaging metadata, script, and documentation here.
