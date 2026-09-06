<!-- SPDX-License-Identifier: Apache-2.0 -->
# goocanvas2

This directory packages GNOME GooCanvas `2.0.4` for openEuler 24.03 LTS SP3
on `riscv64`/RVA23. It intentionally follows the stable 2.x ABI required by
consumers of `goocanvas-2.0`; GooCanvas 3.0 is a separate inventory release
line and is not a compatible substitute for that interface.

The build enables the shared C library, GObject introspection metadata, and
Python 3 PyGObject override. It publishes the `goocanvas-2.0.pc` development
interface needed by dependent packages. The official GNOME archive is pinned
by the SHA-256 published beside the 2.0.4 release in `sources.yaml`, then is
fetched and reverified by target CI.

The 2.0.4 release tree has no functional automated test suite outside its
optional gtk-doc consistency checks. `%check` retains the upstream check target
and adds a compiled, display-independent public-ABI type-registration probe.
The installed smoke test checks the RPM split, the exact pkg-config version,
an installed-header compile/link/run cycle, and Python introspection loading.

No target RPM build or publication is claimed by this package definition.
External source licenses remain those of upstream; the repository license only
covers original packaging metadata and tests.
