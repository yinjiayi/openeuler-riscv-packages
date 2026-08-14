<!-- SPDX-License-Identifier: Apache-2.0 -->
# libltc

This directory packages libltc `1.3.2` for openEuler 24.03 LTS SP3 on
`riscv64`/RVA23. The official upstream `v1.3.2` tag resolves to immutable
commit `bf84b01097a1789c0296cc5fcfc3bf4608407930`; that commit archive is
SHA-256 pinned, single-rooted, and free of unsafe paths, links, or special
members. It contains the upstream LGPL-3.0-or-later license and complete
maintained test corpus.

Arch stable, Debian, Fedora 44 GA, openSUSE Tumbleweed, and Ubuntu provide
frozen cross-distribution lineage. Read-only AUR RPC metadata was considered;
no AUR PKGBUILD or distribution recipe was read or executed. The fixed target
repository has neither this component nor a provider or consumer of its
`libltc.so.11` ABI.

`%check` runs upstream `make check` without omissions. It builds and executes
the encoder, decoder, fixture decoder, 48 kHz and 192 kHz comparison cases,
and loop test. Installed smoke verifies the SONAME and compiles and runs a
client through the public pkg-config and encoder APIs without network access.

External source licenses remain those of upstream. Apache-2.0 covers only the
original packaging metadata, scripts, tests, and documentation here.
