<!-- SPDX-License-Identifier: Apache-2.0 -->
# libthai

This directory packages upstream `https://linux.thai.net/projects/libthai`
version `0.1.30` for openEuler 24.03 LTS SP3 on `riscv64`/RVA23. The source
manifest pins the official stable publisher archive and its SHA-256 digest.

The frozen discovery snapshot is the immutable metadata capture identified by
`discovery-20260808T165000Z-9a89920c269462cd`. It cross-checks Arch stable
`extra` (`0.1.30-1`), Fedora 44 (`0.1.30-2.fc44`), openSUSE Tumbleweed
(`0.1.30-1.5`), Debian stable (`0.1.29-2`), and Ubuntu Resolute GA
(`0.1.30-1`). The same snapshot had no canonical AUR row. No distribution
recipe or AUR content was read or executed.

The complete release-archive gate is `make check`. With the full word-break
dictionary enabled, it executes all nine maintained character, collation,
input, rendering, string, and word-breaking test programs with zero skips.
The suite passed from a clean source tree in a network-isolated native
`riscv64` environment. The built `libthai.so.0.3.2` retains target repository
SONAME 0 while updating the target's 0.1.29 package set.

External source licenses remain those of upstream. The repository's
Apache-2.0 license covers only the original packaging metadata, scripts, and
documentation in this directory.
