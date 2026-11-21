<!-- SPDX-License-Identifier: Apache-2.0 -->
# perl-number-tolerant

This directory packages [Number::Tolerant 1.710](https://metacpan.org/dist/Number-Tolerant)
for openEuler 24.03 LTS SP3 on RISC-V/RVA23. It also contains Test::Tolerant.
The fixed CPAN archive matches the signed PAUSE CHECKSUMS and MetaCPAN
digest. Debian stable and Fedora 44 GA lineage is retained.

The upstream LICENSE retains the original same-Perl grant. A notice-only
patch preserves the original Dist::Zilla 6.029 and version 0.9909 attribution
and the original Apache-2.0 terms for the generated test helpers:

- Dist-Zilla 6.029: SHA-256 928ad03ebb6d20839a5c7d01074c40ba528678ff4d7c93f46909e8b6f38b101a.
- Dist-Zilla-Plugin-Test-ReportPrereqs 0.028: SHA-256 2aa38c5e8498fa6d930c16d6d32d5b57edf776e33fac6a94ea2be4c242cf1be3.
- Dist-Zilla-Plugin-CheckChangesHasContent 0.011: SHA-256 ab970b50349f87975ac7e3d5f0297f8d67e4f6fe09564778f27f42eca27ea154.
- version 0.9909: SHA-256 6998f2eea7985e11cbb8e6fd2a404980c3b187c0bd484c88e2af91e80bedf3fe.

All 27 original default tests run unchanged. The two original TODO
assertions in stringify_as.t are kept. The installed smoke verifies numeric
range matching and the companion test assertion.
