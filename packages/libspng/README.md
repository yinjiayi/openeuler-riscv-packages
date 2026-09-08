<!-- SPDX-License-Identifier: Apache-2.0 -->
# libspng

This directory packages upstream libspng 0.7.4 for openEuler 24.03 LTS SP3
on `riscv64`/RVA23. CI downloads the official release tag over HTTPS and
verifies its pinned SHA-256 before the network-enabled target build.

The package enables the full bundled Meson development suite, including the
PNG reference-image comparisons and malformed-input regressions. The
installed-RPM smoke test compiles and links against `spng.pc`, encodes a
one-pixel image, and verifies its PNG signature.

External source licenses remain BSD-2-Clause and libpng-2.0. The repository
license only covers original packaging metadata, scripts, and documentation.
