<!-- SPDX-License-Identifier: Apache-2.0 -->
# libnet-subnet-perl

This directory packages upstream `https://metacpan.org/dist/Net-Subnet` version `1.03` for openEuler 24.03 LTS SP3 on `riscv64`/RVA23.

External source and patch licenses remain those of their respective upstream projects. The repository license only covers original packaging metadata, scripts, and documentation.

The fixed CPAN source matches the signed PAUSE checksum and the Debian stable original byte for byte. Both complete Perl license texts ship with the original attribution. The upstream MakeMaker default tests are unchanged.

The installed smoke exercises numeric IPv4/IPv6 matching and IPv6 longest-prefix classification. It makes no DNS requests. As documented upstream, callers that supply IPv4 hostnames instead of numeric addresses may trigger the platform resolver.
