<!-- SPDX-License-Identifier: Apache-2.0 -->
# libwbxml

This package maps the inventory's exact `libwbxml` key to the official
[libwbxml 0.11.10 release](https://github.com/libwbxml/libwbxml/releases/tag/libwbxml-0.11.10)
for openEuler 24.03 LTS SP3 on `riscv64`/RVA23. The tag resolves to commit
`e58b1f19f11dbadff53e5b486b8c4b16639a656a`; its HTTPS archive was
independently downloaded and pinned to SHA-256
`027b77ab7c06458b73cbcf1f06f9cf73b65acdbb2ac170b234c1d736069acae4`.
The archive has one top-level source tree and no traversal paths, links, or
special files. CI verifies the pinned hash before building.

The upstream CMake build retains all language converters and enables its
Check-based API tests through `check-devel`. `%check` runs the complete
registered CTest suite: XML corpus round-trips, API checks, and malformed
WBXML regression files. Upstream intentionally excludes DRMREL cases owing
to a broken external specification; this package does not disable any
upstream-registered test. The installed-RPM smoke checks the public header,
shared-library symbol, pkg-config metadata, and both converter commands.
It is narrower than the complete upstream CTest suite.

The packaged library and tools retain the upstream LGPL-2.1-or-later grant.
The source archive also contains unused GPL/BSD/MIT-licensed material; it is
not installed into the binary RPMs. CI build artifacts are not evidence of
publication to the public RPM repository.
