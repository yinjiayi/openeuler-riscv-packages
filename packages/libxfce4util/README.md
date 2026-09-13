<!-- SPDX-License-Identifier: Apache-2.0 -->
# libxfce4util

This directory packages the official Xfce `libxfce4util` 4.20 stable release
`4.20.1` for openEuler 24.03 LTS SP3 on `riscv64`/RVA23. The library provides
non-GUI utilities shared by Xfce applications, including the
`libxfce4util-1.0` pkg-config interface required to build `xfconf`.

The source is served by the direct `archive.fr.xfce.org` HTTPS mirror named by
Xfce's canonical archive service, and its independently computed SHA-256
matches the checksum published by Xfce. The direct mirror is used because the
repository downloader advertises JSON support and the canonical archive
endpoint answers that request with mirror-selection metadata rather than the
archive bytes. The archive has one top-level
directory, no parent traversal or absolute paths, no links, and no special
device or FIFO entries. The Meson build keeps GObject introspection enabled and
makes the upstream Vala binding option mandatory. Its direct GLib, GObject,
GIO, introspection, Vala, gettext, compiler, Meson, Ninja, and Python interfaces
are declared directly. The repository metadata fixed by `ci/image.lock` maps
the four pkg-config interfaces to `glib2-devel` 2.78.3 and
`gobject-introspection-devel` 1.76.1. Python runs the `xdt-gen-visibility`
generator shipped in the verified source archive.

Upstream 4.20.1 registers no Meson test cases. `%check` still invokes the
upstream Meson test entry point and then executes the built
`xfce4-kiosk-query -v` path. The installed smoke test verifies both that binary
and the RPM-generated `pkgconfig(libxfce4util-1.0)` provider. A successful
exact-head target CI run is still required before changing the RISC-V status
from `unknown` or treating this package as a published prerequisite.

The installed library sources use LGPL-2.0-or-later terms, while the kiosk
query and several library integration sources use GPL-2.0-or-later terms.
`xdt-gen-visibility` is a GPL-3.0-or-later build-only helper and is not installed
in the binary RPM.

External source licenses remain those of the upstream project. The repository
license only covers original packaging metadata, scripts, and documentation.
