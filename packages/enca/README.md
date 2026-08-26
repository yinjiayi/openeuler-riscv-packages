<!-- SPDX-License-Identifier: Apache-2.0 -->
# enca

This directory packages Enca 1.22 for openEuler 24.03 LTS SP3 on
riscv64/RVA23. Enca consists of the charset-analyzing `libenca` library and
the `enca`/`enconv` conversion front ends. The immutable discovery snapshot
`discovery-20260808T165000Z-9a89920c269462cd` records Arch stable and
metadata-only AUR at 1.22, Ubuntu GA at 1.21, and Debian stable, Fedora 44 GA,
and openSUSE Tumbleweed at 1.19. No AUR recipe or distribution packaging
script was read or executed.

The maintained official repository moved to Project OSS Revival. Its current
stable 1.22 release asset is pinned by SHA-256, and the calculated digest
matches GitHub's publisher digest. Pre-extraction inspection found one root,
no links or special entries, and no unsafe path. Enca's implementation is
GPL-2.0-only; its installed public header explicitly states public-domain
status, reflected in the RPM license expression.

The full upstream check gate enables librecode and external conversion so all
21 bundled tests, including TeX, recode, iconv, locale, and error paths, run
without a skip. Installed smoke verifies the selected converter, command
version, pkg-config metadata, and public library API. The fixed target has
Enca 1.19-1 and `libenca.so.0`; version 1.22 is a higher EVR and preserves the
same SONAME. All BuildRequires are present. Target RPM, install, and smoke
status remains unknown until exact-head QEMU CI completes.

External source licenses remain upstream's. Apache-2.0 covers only this
repository's original packaging metadata, scripts, tests, and documentation.
