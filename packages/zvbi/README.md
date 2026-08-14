<!-- SPDX-License-Identifier: Apache-2.0 -->
# zvbi

This directory packages ZVBI 0.2.44 for openEuler 24.03 LTS SP3 on
riscv64/RVA23. Fedora 44, Arch stable, Debian stable, openSUSE Tumbleweed, and
Ubuntu all independently track 0.2.44. AUR was queried only through its
read-only RPC for lib32-zvbi metadata; no PKGBUILD, install hook, patch, or
command from AUR was read or executed.

Upstream's signed v0.2.44 tag was resolved to commit
5169a428d51c3ae8ff7b0897e8a687d8e05e37b5, and that immutable official
repository archive is pinned by SHA-256. Archive inspection found one root and
no absolute path, parent traversal, link, or special entry. This release
includes upstream security fixes and retains libzvbi.so.0, matching the
openEuler target's existing ABI major.

The SPEC explicitly keeps tests and examples enabled, then runs the complete
top-level `make check` gate. This covers the C/C++ header matrix, PDC, DVB
mux/demux, Hamming, packet, raw-decoder, VPS, Unicode, and example-script
checks; no test is skipped or made non-fatal. The installed smoke test verifies
the reported version and allocates a decoder through the public C API. RISC-V
status remains unknown until the pinned openEuler RVA23/QEMU workflow
completes.

External source licenses remain upstream's. Apache-2.0 covers only this
repository's original packaging metadata, scripts, tests, and documentation.
