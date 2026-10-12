<!-- SPDX-License-Identifier: Apache-2.0 -->
# libcdio-paranoia

This directory packages GNU libcdio-paranoia 10.2+2.0.2 for openEuler
24.03 LTS SP3 on riscv64/RVA23. It upgrades the fixed target's
10.2+2.0.0 build while preserving the existing
`libcdio_cdda.so.2` and `libcdio_paranoia.so.2` ABI provides.

The frozen snapshot `discovery-20260808T165000Z-9a89920c269462cd`
cross-checks Arch Extra 10.2+2.0.2-2, Fedora 44 10.2+2.0.2-6.fc44,
Debian stable 10.2+2.0.2-1, openSUSE 10.2+2.0.1-1.18, Ubuntu Resolute
libcdio 2.2.0-4build1, and AUR metadata for the related immutable
libcdio Android packages. No AUR PKGBUILD or distribution recipe was
read or executed.

The GNU archive is SHA-256 pinned. `make check` runs every shipped
endian, TOC, image, track-range, and paranoia regression test. The spec
also carries Fedora 44's two NULL guards from upstream pull request 52,
which prevent a cleanup crash without altering test selection.

External source licenses remain those of upstream. The repository's
Apache-2.0 license covers only the original packaging metadata, scripts,
and documentation in this directory.
