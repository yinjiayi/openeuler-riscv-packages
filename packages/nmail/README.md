<!-- SPDX-License-Identifier: Apache-2.0 -->
# nmail

This directory packages upstream `https://github.com/d99kris/nmail` version `5.14.12` for openEuler 24.03 LTS SP3 on `riscv64`/RVA23.

Release `5` declares the complete fixed-repository development dependency
closure required by nmail and its bundled libetpan build: ncurses, OpenSSL,
Xapian, SQLite, curl, Expat, Cyrus SASL, zlib, libmagic, and libuuid. All
features remain enabled. CMake is configured explicitly into the build
directory consumed by the build and test macros. The upstream root build does
not register CTest cases in this release; the package retains its existing
CTest invocation unchanged.

External source and patch licenses remain those of their respective upstream projects. The repository license only covers original packaging metadata, scripts, and documentation.
