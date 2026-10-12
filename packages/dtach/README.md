<!-- SPDX-License-Identifier: Apache-2.0 -->
# dtach

This directory packages the official `dtach` 0.9 release for openEuler 24.03
LTS SP3 on `riscv64`/RVA23. The archive is fetched from SourceForge and pinned
by its full SHA-256 digest in `sources.yaml`.

`dtach` is a small terminal session detach/attach utility. AUR and Debian
records are retained as distribution lineage only; their packaging recipes
were not executed. The upstream GPL-2.0-or-later license governs the fetched
source, while Apache-2.0 covers this repository's original packaging files.

The target CI build deliberately has network access so source and build
dependencies can be retrieved at build time. The upstream `%check` probes the
version and help interfaces, and the installed smoke test verifies the same
interfaces from the resulting RPM.
