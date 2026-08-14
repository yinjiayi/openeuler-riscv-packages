<!-- SPDX-License-Identifier: Apache-2.0 -->
# fast-float

This directory packages upstream `https://github.com/fastfloat/fast_float` version `8.2.10` for openEuler 24.03 LTS SP3 on `riscv64`/RVA23.

External source and patch licenses remain those of their respective upstream projects. The repository license only covers original packaging metadata, scripts, and documentation.

The complete upstream unit-test targets run offline with the pinned doctest
2.5.2 release. `FASTFLOAT_SUPPLEMENTAL_TESTS` remains disabled because upstream
retrieves that optional data from the mutable `origin/main` branch rather than
an immutable release; this does not disable the library's maintained unit-test
suite.
