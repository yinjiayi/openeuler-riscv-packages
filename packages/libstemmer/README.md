<!-- SPDX-License-Identifier: Apache-2.0 -->
# libstemmer

This directory packages Snowball libstemmer 3.1.1 for openEuler 24.03 LTS SP3
on riscv64/RVA23. Arch stable confirms 3.1.1, Fedora 44 GA carries the reviewed
3.0.1 baseline, and Debian, openSUSE, and Ubuntu provide older Snowball or
PyStemmer source lineages. The frozen discovery component identifier reflects
the resolver's Snowball-family normalization; the build input is solely the
official Snowball libstemmer C release tarball.

AUR was queried only through read-only RPC for lib32-libstemmer metadata. No
PKGBUILD, install hook, patch, source instruction, or command from AUR was read
or executed. The official Snowball tarball was downloaded independently and
SHA-256 pinned. It has exactly one libstemmer_c-3.1.1 root and no absolute
path, parent traversal, link, or special entry.

The release Makefile produces a static archive and the stemwords reference
program but no shared object and no automated test suite. The SPEC preserves
the existing openEuler libstemmer.so.0 ABI by linking the complete upstream
object set as a shared library, and it adds deterministic stemwords plus public
C API checks rather than claiming or skipping a nonexistent upstream suite.
The installed smoke test repeats the public API check against the packaged
shared library. RISC-V status remains unknown until the pinned openEuler
RVA23/QEMU workflow completes.

External source licenses remain upstream's. Apache-2.0 covers only this
repository's original packaging metadata, scripts, tests, and documentation.
