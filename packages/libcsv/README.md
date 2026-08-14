<!-- SPDX-License-Identifier: Apache-2.0 -->
# libcsv

This directory packages upstream `https://sourceforge.net/projects/libcsv/`
version `3.0.3` for openEuler 24.03 LTS SP3 on `riscv64`/RVA23.

The frozen discovery snapshot is the immutable metadata capture identified by
`discovery-20260808T165000Z-9a89920c269462cd`. It cross-checks AUR
(`3.0.3-1`), Fedora 44 (`3.0.3^20210820gitb1d5212-20.fc44`), openSUSE
Tumbleweed (`3.0.3-2.30`), Debian stable (`3.0.3+dfsg-6`), and Ubuntu
Resolute GA (`3.0.3+dfsg-6build1`). The same snapshot was queried for Arch
stable metadata and contained no `libcsv` component; that negative result is
recorded rather than inventing a lineage row. No distribution recipe or AUR
content was read or executed.

The complete maintained upstream test gate is `make check`. It builds and runs
the publisher archive's parser and writer regression program without network
access. The source is the publisher's immutable stable SourceForge release,
not a substituted distribution copy.

External source licenses remain those of upstream. The repository's
Apache-2.0 license covers only the original packaging metadata, scripts, and
documentation in this directory.
