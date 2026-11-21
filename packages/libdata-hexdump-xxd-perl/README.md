<!-- SPDX-License-Identifier: Apache-2.0 -->
# perl-data-hexdump-xxd

This directory packages [Data::HexDump::XXD 0.1.1](https://metacpan.org/dist/Data-HexDump-XXD)
for openEuler 24.03 LTS SP3 on RISC-V/RVA23. Fedora 44 GA lineage and
the signed fixed CPAN source checksum are retained.

The original README and the installed module carry the same-Perl license
grant. The module's bilingual notices are preserved byte-for-byte. The
example xxd script stays in the source archive and is not installed.

The full upstream default suite runs unchanged, including its two original
author-only POD self-skips. Installed smoke verifies dump grouping and an
exact binary round trip containing both NUL and high-byte values.
