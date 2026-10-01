<!-- SPDX-License-Identifier: Apache-2.0 -->
# Libconfini

This directory packages the official libconfini 1.16.4 release asset with
generated `configure` for openEuler 24.03 LTS SP3 on `riscv64`/RVA23. Its
HTTPS tarball is pinned to SHA-256
`f4ba881e68d0d14f4f11f27c7dd9a9567c549f1bf155f4f8158119fb9bc9efd6`.
All archive members remain under one top-level directory. The bundled hard
links resolve within that directory; there are no absolute or parent-traversal
members. Upstream code is GPL-3.0-or-later; Apache-2.0 governs these packaging
files only.

The default complete upstream `make check` suite runs serially. Its registered
`autotest` checks `strip_ini_cache`; the installed RPM smoke test independently
parses a section and key through `load_ini_path` and the public pkg-config
metadata. The upstream development/performance experiments are not registered
in the default `make check` target and do not establish performance evidence.
Bundled manuals and examples are installed without generating documentation.

Upstream configure temporarily clears distribution `CFLAGS` before an fopen
link probe. With the target's hardened RISC-V default PIE link, this yields
non-PIC relocations and no runnable conftest. The SPEC supplies `gcc -fPIC`
as the compiler for configure and build, preserving the distro flags and all
tests without modifying upstream source or declaring a false cross-build.

The next exact-head CI build completed compilation, installation and the
upstream test, then RPM rejected two installed but unlisted compatibility
headers. The devel manifest now owns `confini-1.h` and `confini-1.16.h` along
with `confini.h`. The runtime manifest already owns the installed documentation
directory; the duplicate `%doc README` directive was removed to avoid duplicate
file-list warnings without dropping that documentation.

The frozen AUR record is discovery lineage only; no external package recipe is
executed. QEMU-user CI covers functional behavior, not native RISC-V timing or
performance. A successful PR build is not evidence of repository publication.
