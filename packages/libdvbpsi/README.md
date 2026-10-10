<!-- SPDX-License-Identifier: Apache-2.0 -->
# libdvbpsi

libdvbpsi 1.3.3 is the latest release in VideoLAN's [official archive](https://download.videolan.org/pub/libdvbpsi/).
The archive SHA-256 matches VideoLAN's adjacent `.sha256` file and is pinned
for the openEuler 24.03 LTS SP3 `riscv64`/RVA23 build. The frozen
cross-distribution discovery only established component lineage; it had no
official checksum. No AUR or distribution packaging recipe was read or
executed. Source headers and COPYING license the library LGPL-2.1-or-later.

The upstream `make check` target does not register `misc/test_dr`, which
exercises 15 DVB descriptors and returns failure on any mismatch. `%check`
runs both. Installed-RPM smoke compiles a public API consumer that creates
and releases a decoder handle and a descriptor. This establishes functional
linkage under QEMU user mode, not hardware or transport timing behavior.
The first CI run at head `f6689740172821b0eef3d8944d39c65e2ff09da7`
built the RPMs and passed descriptor tests, but installed smoke did not compile:
upstream public headers expect consumers to include standard size/type headers
first. The smoke consumer now includes them; a new exact-head CI run is needed.

Apache-2.0 covers original packaging metadata, tests, and this document;
upstream source retains its LGPL terms.
