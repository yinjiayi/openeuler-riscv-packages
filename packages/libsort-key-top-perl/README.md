<!-- SPDX-License-Identifier: Apache-2.0 -->
# libsort-key-top-perl

This directory packages upstream `https://metacpan.org/dist/Sort-Key-Top` version `0.08` for openEuler 24.03 LTS SP3 on `riscv64`/RVA23.

External source and patch licenses remain those of their respective upstream projects. The repository license only covers original packaging metadata, scripts, and documentation.

The authorized official CPAN archive SHA-256 is
`db7c4de42316d7b0d8f14a720a34f266374109a117efc8b67ea7fc498c4113e4`.
It matches the publisher CHECKSUMS signature at signing time.
Debian stable 0.08-4 establishes naming lineage only.

The original README retains Salvador Fandino's same-Perl grant.
The bundled `ppport.h` exactly reproduces from Devel::PPPort 3.08,
and `sort.h` retains the licensed Perl core sort source and its
compatibility adaptations. The binary RPM retains the original
donor notice blocks and both complete pinned Perl license texts;
the SRPM carries the unchanged original source.

The native XS build runs all unchanged upstream default tests.
The installed smoke tests the top-k result and requires the actual
shared object to have loaded.
