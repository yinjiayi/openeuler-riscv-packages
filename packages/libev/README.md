<!-- SPDX-License-Identifier: Apache-2.0 -->
# libev

This directory packages libev 4.33 for openEuler 24.03 LTS SP3
`riscv64`/RVA23. The official [release directory](https://dist.schmorp.de/libev/)
currently lists 4.33 as its stable tarball. The archive was downloaded over
HTTPS and pinned to SHA-256
`507eb7b8d1015fbec5b935f34ebed15bf346bed04a11ab82b8eee848c4205aea`.
All 40 archive entries are regular files or directories beneath the expected
`libev-4.33/` root; none traverses upward. `LICENSE` offers a BSD-2-Clause
or GPL-2.0-or-later choice.

The frozen discovery snapshot records libev 4.33 across Arch, Debian,
Fedora, openSUSE, and Ubuntu. The release is built with the supplied Autotools
configuration for openEuler's target image. Upstream's `make check` target
contains no executable tests, so `%check` additionally compiles and runs a
public-API timer callback. The installed smoke test independently compiles
and runs the same event-loop behavior against the installed shared library.
The target build and installation results remain unknown until CI runs.
