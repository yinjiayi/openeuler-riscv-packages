<!-- SPDX-License-Identifier: Apache-2.0 -->
# libarray-refelem-perl

This directory packages upstream `https://metacpan.org/dist/Array-RefElem` version `1.00` for openEuler 24.03 LTS SP3 on `riscv64`/RVA23.

External source and patch licenses remain those of their respective upstream projects. The repository license only covers original packaging metadata, scripts, and documentation.

The source README attributes the module to Gisle Aas and grants Perl's dual terms. CPAN's PAUSE-signed CHECKSUMS binds the fixed archive SHA-256; this is a PAUSE checksum attestation, not an author signature. The upstream `t/refelem.t` test is preserved via `make test`, and the installed smoke exercises an actual XS array alias. Fedora's public F44 SPEC was consulted for the architecture-specific MakeMaker install path and empty `.bs` handling; no external packaging code was executed. Original tests and installed behavior require target CI; no native build is claimed here.
