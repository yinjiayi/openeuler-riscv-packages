<!-- SPDX-License-Identifier: Apache-2.0 -->
# libnftnl

This directory packages upstream
`https://www.netfilter.org/projects/libnftnl/` version `1.3.1` for openEuler
24.03 LTS SP3 on `riscv64`/RVA23. The source manifest pins the publisher's
stable release archive and its published SHA-256 digest.

The frozen discovery snapshot is the immutable metadata capture identified by
`discovery-20260808T165000Z-9a89920c269462cd`. It cross-checks Arch stable
`core` (`1.3.1-1`), Fedora 44 (`1.3.1-2.fc44`), openSUSE Tumbleweed
(`1.3.1-1.5`), Debian stable (`1.2.9-1`), and Ubuntu Resolute GA (`1.3.1-1`).
The same snapshot had no canonical AUR row. No distribution recipe or AUR
content was read or executed.

The complete release-archive gate is `make check`. It executes all 32
maintained object, rule, set, flowtable, expression, and user-data test cases
with zero skips. The suite passed from a clean source tree in a
network-isolated native `riscv64` environment. The built
`libnftnl.so.11.7.0` retains target repository SONAME 11 while updating the
target's 1.2.6 package set.

External source licenses remain those of upstream. The repository's
Apache-2.0 license covers only the original packaging metadata, scripts, and
documentation in this directory.
