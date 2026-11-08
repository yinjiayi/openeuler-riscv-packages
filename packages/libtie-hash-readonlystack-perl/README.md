<!-- SPDX-License-Identifier: Apache-2.0 -->
# perl-tie-hash-readonlystack

This directory packages upstream `https://metacpan.org/dist/Tie-Hash-ReadonlyStack` version `0.2` for openEuler 24.03 LTS SP3 on `riscv64`/RVA23.

External source and patch licenses remain those of their respective upstream projects. The repository license only covers original packaging metadata, scripts, and documentation.

The fixed CPAN archive SHA-256 matches MetaCPAN and signed PAUSE CHECKSUMS.
The upstream README and vendor POD retain Daniel Muey's original same-Perl
grant. Fedora 44 GA is discovery lineage, not a source substitute.

The original MakeMaker test suite includes the POD and POD coverage tests.
The original author-only PerlCritic test self-skips when its optional
development dependency is absent; no test is removed or excluded. The
installed smoke exercises override and fallback lookups and checks that the
underlying hash remains unchanged.
