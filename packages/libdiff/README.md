<!-- SPDX-License-Identifier: Apache-2.0 -->
# Libdiff

This directory packages upstream libdiff 0.1.0 for openEuler 24.03 LTS SP3
on `riscv64`/RVA23. Official tag `VERSION_0_1_0` resolves to commit
`9f98d020c65e31946edc058494b605ddef26d295`. The HTTPS archive is
SHA-256 pinned as `987d846c28c30da62528558516b2fa015f71f8336381e82e0d16cd605c983f68`.
All archive members are regular files or directories under
`libdiff-VERSION_0_1_0/`, with no absolute path or parent traversal.

The core library is MIT licensed. Compatibility code also contains
BSD-3-Clause and ISC notices; the source and notices are retained. The AUR
discovery record was classified stale, but the official 0.1.0 tag is still
the newest tag on 2026-09-28. No AUR recipe is executed. Automatic updates
are disabled because the `VERSION_0_1_0` tag syntax cannot be mapped from
the RPM version by this repository's source URL template; future releases
require manual review.

Upstream `tests.c` contains configure feature probes, not a runtime suite.
The package `%check` runs the built character and word difference tools on
known inputs. Installed smoke additionally compiles and links a C consumer
against the static library and verifies edit distance and common-subsequence
length. Passing QEMU-user CI does not establish native RISC-V performance or
RPM repository publication.
