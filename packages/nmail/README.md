<!-- SPDX-License-Identifier: Apache-2.0 -->
# nmail

This directory packages upstream `https://github.com/d99kris/nmail` version `5.14.12` for openEuler 24.03 LTS SP3 on `riscv64`/RVA23.

Release `6` declares the complete fixed-repository development dependency
closure required by nmail and its bundled libetpan build: ncurses, OpenSSL,
Xapian, SQLite, curl, Expat, Cyrus SASL, zlib, libmagic, and libuuid. All
features remain enabled. CMake is configured explicitly into the build
directory consumed by the build macros. The package explicitly owns the nmail
binary and compression-tolerant manual path so RPM post-processing cannot
invalidate a pre-generated file manifest. The upstream root build does not
register CTest cases in this release, so `%check` executes the upstream release
smoke contract: the build-tree binary must answer `--version` with the packaged
version and successfully display `--help`.

External source and patch licenses remain those of their respective upstream projects. The repository license only covers original packaging metadata, scripts, and documentation.
