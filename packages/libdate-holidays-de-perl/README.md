<!-- SPDX-License-Identifier: Apache-2.0 -->
# libdate-holidays-de-perl

This directory packages upstream `https://metacpan.org/dist/Date-Holidays-DE` version `2.07` for openEuler 24.03 LTS SP3 on `riscv64`/RVA23.

External source and patch licenses remain those of their respective upstream projects. The repository license only covers original packaging metadata, scripts, and documentation.

The original README contains the complete ISC grant and contributor notice.
The recipe runs the upstream default `test.pl` unchanged. The installed
smoke separately checks fixed historical date and state behavior in UTC; it
does not assert that the release covers current or future holiday changes.
