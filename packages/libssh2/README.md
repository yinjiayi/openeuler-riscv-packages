<!-- SPDX-License-Identifier: Apache-2.0 -->
# libssh2

This directory packages libssh2 1.11.1 for openEuler 24.03 LTS SP3 on
`riscv64`/RVA23. The source is the official upstream archive at
`https://libssh2.org/download/libssh2-1.11.1.tar.gz`; it is pinned by SHA-256
in `sources.yaml` as
`d9ec76cbe34db98eec3539fe2c899d26b0c837cb3eb466a56b0f109cabf658f7`.
The archive has one top-level directory and 462 total members, including 446
regular files and 16 directories. It has no absolute or parent-traversal
paths, links, or special files. The same bytes were
also fetched from the matching GitHub release asset.

The frozen discovery snapshot
`discovery-20260808T165000Z-9a89920c269462cd` corroborates libssh2 1.11.1
across Arch stable, AUR metadata, Debian stable, Fedora GA, openSUSE
Tumbleweed, and Ubuntu GA. AUR and distribution recipes are retained only as
untrusted lineage evidence; none is executed or used as a source archive.

The SPEC builds the shared library with the OpenSSL crypto backend and zlib
compression, while retaining the upstream static library only long enough to
link tests. The installed package contains the shared ABI, headers, CMake and
pkg-config metadata, and manual pages. `%check` runs the upstream CMake suite
with the local OpenSSH fixture; only tests that require starting a nested
Docker daemon are disabled because the CI build container cannot provide that
privileged service. The installed smoke test compiles and runs a public API
consumer.

External source licenses remain those of libssh2. Apache-2.0 covers only this
repository's original packaging metadata and smoke test.
