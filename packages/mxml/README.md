<!-- SPDX-License-Identifier: Apache-2.0 -->
# mxml

This directory packages upstream `https://www.msweet.org/mxml/` version
`4.0.4` for openEuler 24.03 LTS SP3 on `riscv64`/RVA23.

The frozen discovery snapshot is the immutable metadata capture identified by
`discovery-20260808T165000Z-9a89920c269462cd`. It cross-checks Arch stable
`extra` (`3.3.1-2`), Fedora 44 (`3.3.1-10.fc44`), openSUSE Tumbleweed
(`3.3.1-1.12`), Debian stable (`3.3.1-1+deb13u1`), and Ubuntu Resolute GA
(`3.3.1-1build2`). The same snapshot was queried for AUR metadata and contained
no `mxml` component; that negative result is recorded rather than inventing a
lineage row. No distribution recipe or AUR content was read or executed.

The full upstream test gate is the maintained `make test` target from the
publisher archive. It exercises file, string, and file-descriptor parsing and
serialization, including byte-for-byte round trips, without network access.
The archive is the publisher-generated stable release asset, not a substituted
distribution copy.

External source licenses remain those of upstream. The repository's
Apache-2.0 license covers only the original packaging metadata, scripts, and
documentation in this directory.
