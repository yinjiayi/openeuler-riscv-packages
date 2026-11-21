<!-- SPDX-License-Identifier: Apache-2.0 -->
# libtie-refhash-weak-perl

This directory packages upstream `https://metacpan.org/dist/Tie-RefHash-Weak` version `0.09` for openEuler 24.03 LTS SP3 on `riscv64`/RVA23.

External source and patch licenses remain those of their respective upstream projects. The repository license only covers original packaging metadata, scripts, and documentation.

The original copyright and dual-license notice remain in the installed
`Tie/RefHash/Weak.pm`; the package includes both official full Perl license
texts. The release archive matches the signed PAUSE checksum, the embedded
author manifest, and the Debian stable original source archive.

The original five test files and their upstream non-closure garbage-collection
TODO remain unchanged. The installed smoke separately verifies that a hash
entry is removed once its reference key leaves scope.
