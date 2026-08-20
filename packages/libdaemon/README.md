<!-- SPDX-License-Identifier: Apache-2.0 -->
# libdaemon

This directory packages the official `libdaemon` 0.14 release for openEuler
24.03 LTS SP3 on `riscv64`/RVA23. CI fetches the declared HTTPS archive and
checks its pinned SHA-256 before the network-enabled target build.

The package provides the versioned library and a development subpackage. The
upstream archive has no runnable test suite; `%check` retains its upstream
`make check` target, and the installed-RPM smoke test exercises the public
non-blocking-file-descriptor and identifier APIs without requiring a daemon,
PID file, or privileged operation.

The upstream archive is LGPL-2.1-or-later. The repository license covers only
the original packaging metadata, scripts, and documentation.
