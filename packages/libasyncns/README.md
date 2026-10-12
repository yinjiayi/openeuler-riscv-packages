<!-- SPDX-License-Identifier: Apache-2.0 -->
# libasyncns

This directory packages the official `libasyncns` 0.8 release for openEuler
24.03 LTS SP3 on `riscv64`/RVA23. CI fetches the declared HTTPS archive and
checks its pinned SHA-256 before the network-enabled target build.

The package provides the versioned asynchronous name-service library and a
development subpackage. The upstream `make check` target is retained; it
builds the shipped asynchronous-query test program. The installed-RPM smoke
test exercises session creation and the public descriptor/query-count API
without depending on an external DNS name.

The upstream archive is LGPL-2.1-or-later. The repository license covers only
the original packaging metadata, scripts, and documentation.
