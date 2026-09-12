<!-- SPDX-License-Identifier: Apache-2.0 -->
# lzip

This directory packages upstream `https://www.nongnu.org/lzip/lzip.html`
version `1.26` for openEuler 24.03 LTS SP3 on `riscv64`/RVA23.

The frozen discovery snapshot is the immutable metadata capture identified by
`discovery-20260808T165000Z-9a89920c269462cd`. It cross-checks Arch stable
`extra` (`1.26-1`), Fedora 44 (`1.26-1.fc44`), openSUSE Tumbleweed
(`1.26-1.4`), Debian stable (`1.25-3`), and Ubuntu Resolute GA
(`1.26~rc1-2`). The same snapshot was queried for AUR metadata and contained
no `lzip` component; that negative result is recorded rather than inventing a
lineage row. No distribution recipe or AUR content was read or executed.

The complete upstream test gate is `make check`. Its maintained publisher
script covers compression and decompression, stream listing, stdin/stdout and
file handling, invalid options, malformed headers, truncated streams, and
corruption detection without network access. The official 1.26 archive was
also exercised in a network-isolated native `riscv64` environment.

External source licenses remain those of upstream. The repository's
Apache-2.0 license covers only the original packaging metadata, scripts, and
documentation in this directory.
