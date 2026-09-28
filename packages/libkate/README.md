<!-- SPDX-License-Identifier: Apache-2.0 -->
# libkate

The Xiph [official release archive](https://downloads.xiph.org/releases/kate/)
lists libkate 0.4.3 as the newest stable release. Its HTTPS source tarball is
SHA-256 pinned and contains only regular files and directories in one root.
The frozen Arch/Debian/Fedora metadata is discovery lineage, not an executable
packaging recipe. Upstream COPYING identifies BSD-3-Clause licensing.

This package targets openEuler 24.03 LTS SP3 on `riscv64`/RVA23. It retains
Kate, Ogg-Kate, PNG-enabled encoding, and the three command-line tools. The
optional wxPython/oggz-based KateDJ GUI is installed by upstream only when
both dependencies are present; it is not a core codec feature. `%check` runs
all six registered upstream unit tests, upstream Kate/Ogg and SRT/LRC round
trips, and a directly checked CLI round trip. Installed-RPM smoke links both
shared libraries and checks their public API. QEMU user-mode tests are not
native-hardware performance evidence.

Apache-2.0 covers original packaging metadata, tests, and this document;
upstream source retains BSD-3-Clause terms.
