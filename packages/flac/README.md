<!-- SPDX-License-Identifier: Apache-2.0 -->
# flac

This directory packages FLAC `1.5.0` for openEuler 24.03 LTS SP3 on
`riscv64`/RVA23. Fedora 44, Arch stable, openSUSE Tumbleweed, Debian stable,
and Ubuntu 26.04 LTS GA independently confirm the 1.5.0 release line. Debian
and Ubuntu use repacked `+ds` source revisions; this package uses the pristine
official Xiph release archive.

The downloaded archive's SHA-256 exactly matches Xiph's published
`SHA256SUMS.txt`, and archive inspection found one expected root, safe paths
and links, and no special entries. AUR was queried through RPC only, and no
AUR recipe was read or executed. Distribution specs were reviewed only as
untrusted, read-only lineage evidence and were never executed. The network-free
build preserves Ogg, C++, examples, programs, documentation, shared-library,
and test support. Unlike Fedora's downstream spec, it does not lower
`FLAC__TEST_LEVEL`; the complete level-1 CTest suite runs serially. The
installed smoke test performs a real raw-audio encode/decode round-trip and
links against the installed public C API.

External source licenses remain those of the upstream project. The repository
license covers only original packaging metadata, scripts, and documentation.
