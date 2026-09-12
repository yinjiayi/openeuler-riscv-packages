<!-- SPDX-License-Identifier: Apache-2.0 -->
# libotr

This directory packages the official libotr 4.1.1 stable release for
openEuler 24.03 LTS SP3 on riscv64/RVA23.

The frozen discovery snapshot `discovery-20260808T165000Z-9a89920c269462cd`
cross-checks Arch Extra 4.1.1-6, AUR metadata for the related pidgin-otr
4.0.2-6 consumer, Fedora 44 4.1.1-25.fc44, Debian stable 4.1.1-6,
openSUSE 4.1.1-4.14, and Ubuntu Resolute pidgin-otr 4.0.2-6build1. AUR was
queried only through read-only metadata; no PKGBUILD or distribution recipe
was read or executed.

The official HTTPS release archive is SHA-256 pinned. The complete Linux
upstream unit and regression suites run through `make check`. The regression
client receives the Fedora 44 `sys/socket.h` declaration-only portability fix
from
`https://src.fedoraproject.org/rpms/libotr/raw/f44/f/libotr-4.1.1-socket-h.patch`;
no test is removed, skipped, or weakened.

External source licenses remain those of upstream. The repository's
Apache-2.0 license covers only the original packaging metadata, scripts, and
documentation in this directory.
