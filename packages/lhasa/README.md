<!-- SPDX-License-Identifier: Apache-2.0 -->
# lhasa

This directory packages upstream `https://github.com/fragglet/lhasa`
version `0.6.0` for openEuler 24.03 LTS SP3 on `riscv64`/RVA23.

The frozen snapshot `discovery-20260808T165000Z-9a89920c269462cd`
cross-checks Arch Extra `0.5.0-1`, Fedora 44 `0.5.0-1.fc44`, Debian stable
`0.4.0-1`, Ubuntu Resolute `0.5.0-1`, and openSUSE Tumbleweed `0.6.0-1.3`.
These are exact `lhasa` lineage rows; no external packaging script was read as
executable content or executed.

GitHub marks `v0.6.0` as the current stable, non-prerelease release. The
publisher asset carries GitHub's SHA-256 digest
`9840154367f73e9d9c3196f944a121ab4d398d84e921c8fe8fca8a931274aed7`,
which matches the locally verified bytes. It is a single-root archive with no
unsafe paths, links, or special files. CI fetches and verifies this pinned
source during the network-enabled build. `%check` runs every compiled CRC,
reader, and decoder unit plus all decompression, header, listing, printing,
dry-run, extraction, OS-format, and regression archive corpora. Upstream
deliberately clears `CFLAGS` for unoptimized test-only objects; exact-head run
`31761326968` showed that this conflicts with openEuler's PIE linker on
RISC-V. The SPEC restores only `-fPIE` for those test objects and leaves the
test corpus unchanged. Fresh exact-head CI remains the target authority.

External source licenses remain those of upstream. The repository's
Apache-2.0 license covers only the original packaging metadata, scripts, and
documentation in this directory.
