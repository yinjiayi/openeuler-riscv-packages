<!-- SPDX-License-Identifier: Apache-2.0 -->
# zvbi

This directory packages ZVBI 0.2.45 release 3 for openEuler 24.03 LTS SP3 on
riscv64/RVA23. The frozen discovery snapshot records that Fedora 44, Arch
stable, Debian stable, openSUSE Tumbleweed, and Ubuntu independently tracked
0.2.44. AUR was queried only through its
read-only RPC for lib32-zvbi metadata; no PKGBUILD, install hook, patch, or
command from AUR was read or executed.

The official upstream v0.2.45 tag archive is pinned by SHA-256. Archive
inspection found the single `zvbi-0.2.45` root and no absolute path or parent
traversal entry. The SPEC uses that exact root while retaining libzvbi.so.0,
matching the openEuler target's existing ABI major.

The SPEC explicitly keeps tests and examples enabled, then runs the complete
top-level `make check` gate. This covers the C/C++ header matrix, PDC, DVB
mux/demux, Hamming, packet, raw-decoder, VPS, Unicode, and example-script
checks; no test is skipped or made non-fatal. Upstream documents Doxygen as an
optional API-documentation generator, and this package does not ship its HTML
output, so the SPEC explicitly disables that output rather than pulling its
demonstrated 333-package dependency transaction. The installed library,
commands, examples, tests, headers, and manual pages are unchanged. The
installed smoke test verifies version 0.2.45 and allocates a decoder through
the public C API. RISC-V status remains unknown until the pinned openEuler
RVA23/QEMU workflow completes.

External source licenses remain upstream's. Apache-2.0 covers only this
repository's original packaging metadata, scripts, tests, and documentation.
