<!-- SPDX-License-Identifier: Apache-2.0 -->
# libconvert-ascii85-perl

This directory packages upstream `https://metacpan.org/release/MAUKE/Convert-Ascii85-0.01` version `0.01` for openEuler 24.03 LTS SP3 on `riscv64`/RVA23.

The upstream archive is pinned to the SHA-256 recorded by MetaCPAN and the signed
PAUSE CHECKSUMS entry. The original README notice and full linked Perl license
texts are installed as licenses. No source patch or native-only dependency is used.

The original MakeMaker default suite runs in full, including both POD tests.
Their dependencies are explicit so neither default file silently skips.
The installed smoke test checks the RPM capability, version, zero compression,
and round-tripping binary data through the public API.

External source and patch licenses remain those of their respective upstream projects. The repository license only covers original packaging metadata, scripts, and documentation.
