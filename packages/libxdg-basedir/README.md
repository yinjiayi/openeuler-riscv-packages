<!-- SPDX-License-Identifier: Apache-2.0 -->
# libxdg-basedir

This directory packages upstream
`https://github.com/devnev/libxdg-basedir` version `1.2.3` for openEuler
24.03 LTS SP3 on `riscv64`/RVA23. Official tag `libxdg-basedir-1.2.3`
resolves to immutable commit `b978568d1b3ee04e8197f23ca4e3abdd372f85e1`;
the source manifest pins that commit archive.

The frozen discovery snapshot is the immutable metadata capture identified by
`discovery-20260808T165000Z-9a89920c269462cd`. It cross-checks Arch stable
`extra` (`1.2.3-3`), Fedora 44 (`1.2.0-37.fc44`), openSUSE Tumbleweed
(`1.2.3-2.5`), Debian stable (`1.2.0-2.1`), and Ubuntu Resolute GA
(`1.2.0-2.4`). The snapshot had no canonical AUR row. No distribution recipe
or AUR content was read or executed.

The complete upstream gate regenerates the build system from the vendored
Autoconf macros and runs `make check`. It executes all 31 maintained cache,
configuration, data, search-path, and runtime-directory query cases with zero
skips. The same suite passed from a clean source tree in a network-isolated
native `riscv64` environment. SONAME `libxdg-basedir.so.1` is provided by the
upstream 1.2.3 interface version.

External source licenses remain those of upstream. The repository's
Apache-2.0 license covers only the original packaging metadata, scripts, and
documentation in this directory.
