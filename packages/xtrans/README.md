<!-- SPDX-License-Identifier: Apache-2.0 -->
# xtrans

This package tracks X.Org's official stable `xtrans` 1.6.0 release for
openEuler 24.03 LTS SP3 on `riscv64`/RVA23. The
[X.Org release announcement](https://lists.x.org/archives/xorg-announce/2025-March/003588.html)
publishes SHA-256 `faafea166bf2451a173d9d593352940ec6404145c5d1da5c213423ce4d359e92`,
which matches the independently downloaded HTTPS archive. CI fetches and
rechecks the pinned source. The outer archive has a single source directory
and no links or special files.

Upstream explicitly defines xtrans as shared source and headers compiled into
consuming X.Org components, not as a shared library. Accordingly the RPM is
`noarch` and installs seven source/header files, `xtrans.m4`, and `xtrans.pc`.
The archive has no registered test programs; `%check` preserves its `make
check` target without claiming an upstream suite, while the installed-RPM
smoke compiles the installed transport implementation for a socket-backed
consumer, then compiles and executes a program using the installed header and
pkg-config flags. The smoke cannot validate each consuming X server or library.

`COPYING` and source headers contain several permissive X.Org license
variants; the package records a conservative SPDX conjunction instead of
describing all files as plain MIT. The frozen inventory's exact `xtrans` key
maps to this package ID. PR build artifacts are not evidence of public RPM
publication.
