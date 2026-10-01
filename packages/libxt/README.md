<!-- SPDX-License-Identifier: Apache-2.0 -->
# libXt

This package maps the frozen inventory's exact `libxt` key to X.Org's
stable `libXt` 1.3.1 release for openEuler 24.03 LTS SP3 on `riscv64`/RVA23.
The [official release announcement](https://lists.x.org/archives/xorg-announce/2024-November/003560.html)
publishes SHA-256 `e0a774b33324f4d4c05b199ea45050f87206586d81655f8bef4dba434d931288`
for the HTTPS tarball, matching the independently downloaded file. Its 431
archive members stay under one top-level directory, with no traversal paths,
symlinks, or special files. CI verifies the pinned digest before building.

The upstream Autotools release registers three GLib unit-test executables:
`Alloc`, `Converters`, and `Event`. `glib2-devel` and `--enable-unit-tests`
keep the complete suite active in `%check`; none of these tests needs an X
server. Installed-RPM smoke additionally compiles against the public
`Intrinsic.h` header, links `libXt`, and exercises display-free allocation.
It does not establish X-server protocol coverage.

The exact PR #2153 head `376e679b4bbe0c5fbde3e006311e89f1bcaee520`
ran Package CI `36478534871` on the RVA23 `riscv64` QEMU user-mode target.
`Converters` and `Event` passed, but `Alloc` failed at its fifth of 18
registered cases, `XtMalloc/oversize`: the test expected a NULL allocation
result and received a non-NULL pointer. The original test relies on
`RLIMIT_AS` to constrain the address space before making oversized
allocations. QEMU linux-user does not enforce that guest limit, so the test
precondition was absent. The other 13 `Alloc` cases did not finish because
the GLib harness bailed out. The installed-RPM smoke did not run. This is a
QEMU validation limitation, not a passing upstream test or published RPM.
The package therefore has `needs-native-riscv` build policy; the current CI
intentionally blocks merge instead of hiding the failure. To clear it, run
the unchanged three upstream test programs, all 18 `Alloc` cases, and the
installed-RPM smoke on a real openEuler 24.03 LTS SP3 RVA23 `riscv64` host.
No `LD_PRELOAD` allocator shim or test skip is used.

Optional DocBook specifications are disabled, while the shared library,
public headers, pkg-config interface, and manual pages remain enabled. The
RPM SPDX expression reflects the MIT, historical X11/HPND, and Open Group
notices in upstream `COPYING`. CI artifacts alone do not establish public
RPM repository publication.
