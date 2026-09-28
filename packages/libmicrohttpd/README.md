<!-- SPDX-License-Identifier: Apache-2.0 -->
# libmicrohttpd

This directory packages GNU libmicrohttpd 1.0.10 for openEuler 24.03 LTS SP3
`riscv64`/RVA23. The [live GNU FTP release directory](https://ftp.gnu.org/gnu/libmicrohttpd/)
lists 1.0.10 as the latest 1.x stable tarball; libmicrohttpd 2.x remains an
experimental series. The official primary FTP download and a GNU-selected
mirror were byte-identical, with SHA-256
`04bfe8ef75db7d629a33de767599765cecadc56274a39822d5d081030d577685`.
All 3,357 archive entries are regular files or directories without path
traversal. With HTTPS enabled, the source is LGPL-2.1-or-later per `COPYING`.

The frozen discovery snapshot records libmicrohttpd across Arch, Debian,
Fedora, openSUSE, and Ubuntu. The target openEuler repository also contains
an older 0.9.77 RPM; this PR does not claim an installed upgrade until CI
proves it. The package builds GnuTLS HTTPS support and ensures the libcurl- and
HTTPS-backed upstream default test programs are actually built and run by
`make check`. The optional heavy timing/performance suite explicitly asks for
a dedicated native host and is not enabled on QEMU. The installed smoke test
links a public C client, checks its version, and verifies the TLS feature.
Actual target build and installation outcomes remain unknown until CI runs.
