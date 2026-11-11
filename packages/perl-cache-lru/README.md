<!-- SPDX-License-Identifier: Apache-2.0 -->
# perl-cache-lru

This directory packages upstream `https://metacpan.org/dist/Cache-LRU` version `0.04` for openEuler 24.03 LTS SP3 on `riscv64`/RVA23.

External source and patch licenses remain those of their respective upstream projects. The repository license only covers original packaging metadata, scripts, and documentation.

The fixed CPAN release archive is SHA-256 pinned in `sources.yaml`. Its digest was independently matched to the PAUSE-signed CPAN `CHECKSUMS`; that signature authenticates the PAUSE index, not an individual author signature. The original two `t/*.t` tests remain in `%check`. The installed smoke exercises version, eviction and lookup; target execution and binary artifacts require CI.

The source archive includes Module::Install 1.00 (Adam Kennedy and contributors) and Module::Install::ReadmeFromPod 0.12 (copyright 2010 Chris Williams). Their bundled `inc` files were byte-compared against the corresponding official CPAN releases. Both releases state the same Perl terms. The bundled build helpers are source/build-time content, not separately installed runtime modules.
