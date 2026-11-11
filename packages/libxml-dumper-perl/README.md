<!-- SPDX-License-Identifier: Apache-2.0 -->
# libxml-dumper-perl

This noarch package provides [XML::Dumper](https://metacpan.org/dist/XML-Dumper)
0.81 for openEuler 24.03 LTS SP3 on `riscv64`/RVA23. The fixed CPAN
release is pinned in `sources.yaml`; [Debian stable](https://packages.debian.org/stable/libxml-dumper-perl)
provides naming lineage. The original README is installed unchanged as
license evidence. The 0.81 module retains attribution to original author
Jonathan Eisenzopf, whose original 0.4 archive independently confirms
the same-Perl grant (SHA-256 `0b5c18be1ffbc59be280b29c864d37d73df141a213648aa1fa01e25b6762c8b9`).

The offline build runs all original default tests, including gzip and
UTF-8. Installed smoke serializes and parses both plain XML and actual
gzip-compressed XML.

External source and patch licenses remain those of their respective upstream projects. The repository license only covers original packaging metadata, scripts, and documentation.
