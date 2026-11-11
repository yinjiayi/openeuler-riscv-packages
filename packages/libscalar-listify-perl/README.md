<!-- SPDX-License-Identifier: Apache-2.0 -->
# libscalar-listify-perl

This directory packages upstream `https://metacpan.org/dist/Scalar-Listify` version `0.03` for openEuler 24.03 LTS SP3 on `riscv64`/RVA23.

External source and patch licenses remain those of their respective upstream projects. The repository license only covers original packaging metadata, scripts, and documentation.

The fixed source matches the signed PAUSE checksum and the Debian stable original byte for byte. Both complete Perl license texts and the upstream attribution are included.

The original legacy test runs unchanged: one module-loading assertion and the two original Data::Dumper examples. The separate install smoke checks zero, empty arrays, order and preservation of the original array. References other than array references are outside the documented API and may produce a Data::Dumper warning.
