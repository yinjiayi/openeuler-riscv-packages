<!-- SPDX-License-Identifier: Apache-2.0 -->
# libXtst

This package maps the inventory's exact `libxtst` key to X.Org's official
stable `libXtst` 1.2.5 release for openEuler 24.03 LTS SP3 on
`riscv64`/RVA23. The [release announcement](https://lists.x.org/archives/xorg-announce/2024-August/003525.html)
publishes SHA-256 `b50d4c25b97009a744706c1039c598f4d8e64910c9fde381994e1cae235d9242`
for the HTTPS tarball, matching the independently downloaded source. The
archive has one top-level source tree and no traversal paths, links, or
special files. CI fetches and verifies the pinned hash before building.

The upstream Autotools release registers no automated tests. `%check` keeps
`make check` without claiming a functional upstream suite. The installed-RPM
smoke checks package version, then compiles, links, loads, and runs a client
referencing both the XTest and XRecord public APIs. This does not exercise
protocol operations against a live X server, which remains untested in the
headless QEMU-user CI. No core feature is disabled.

The upstream `COPYING` includes Open Group, Network Computing Devices, Red
Hat, and X Consortium notices, represented conservatively by the RPM's
combined license expression. The devel package includes both public headers,
pkg-config metadata, manual pages, and source DocBook specifications. CI
build artifacts are not evidence of publication to the public RPM repository.
