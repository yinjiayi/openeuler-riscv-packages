<!-- SPDX-License-Identifier: Apache-2.0 -->
# libtie-shadowhash-perl

This directory packages upstream `https://metacpan.org/dist/Tie-ShadowHash` version `2.01` for openEuler 24.03 LTS SP3 on `riscv64`/RVA23.

External source and patch licenses remain those of their respective upstream projects. The repository license only covers original packaging metadata, scripts, and documentation.

The original `LICENSE` records the Perl dual grant, MIT, and FSFAP at file
scope, including the Stanford test support. The two full Perl license texts
are included. The release archive matches signed PAUSE and Debian stable.

The recursive upstream default suite retains all twelve test files. Forty-six
functional assertions run by default; eleven author/release-only files keep
their original skip conditions. The separate installed smoke verifies lookup
precedence, override and deletion without mutating either source.
