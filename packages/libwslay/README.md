<!-- SPDX-License-Identifier: Apache-2.0 -->
# libwslay

This directory packages upstream `https://github.com/tatsuhiro-t/wslay`
version `1.1.1` for openEuler 24.03 LTS SP3 on `riscv64`/RVA23.

The frozen discovery snapshot is
`discovery-20260808T165000Z-9a89920c269462cd`. It cross-checks Arch Extra
`1.1.1-7`, AUR metadata-only `lib32-libwslay` `1.1.1-1`, Fedora 44
`1.1.1-8.fc44`, Debian stable `1.1.1-4`, openSUSE Tumbleweed `1.1.1-2.20`,
and Ubuntu Resolute `1.1.1-5`. No AUR recipe or distribution build script
was read as executable content or executed.

The current stable `release-1.1.1` tag archive is pinned at SHA-256
`7b9f4b9df09adaa6e07ec309b68ab376c0db2cfd916613023b52a47adfda224a`.
It is a single-root archive with no unsafe paths, links, or special files.
The tag archive is deliberately used instead of the smaller generated dist
asset because it retains the session and stack tests. The tag tree's Autotools
files are regenerated locally from the shipped `configure.ac` and
`Makefile.am` files. `%check` runs the Automake suite and the tag's complete
CMake/CUnit frame, event, queue, session, and stack suite with no build-time
network.

External source licenses remain those of upstream. The repository's
Apache-2.0 license covers only the original packaging metadata, scripts, and
documentation in this directory.
