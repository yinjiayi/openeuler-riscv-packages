<!-- SPDX-License-Identifier: Apache-2.0 -->
# libsafe-isa-perl

Package Safe::Isa 1.000010 for openEuler 24.03 LTS SP3, riscv64/RVA23.
The unchanged official CPAN source matches the signed PAUSE checksum
manifest, the Debian stable original, and the source and test files at
upstream tag v1.000010. The original author notice and both complete
Perl license texts are installed; the repository license only covers
original packaging material.

The recipe builds without network access and requires the release's
original META.yml before Makefile.PL, so the dormant developer-only
Distar acquisition path is not invoked. The default MakeMaker tests
remain unchanged. The installed smoke checks safe object introspection,
non-object handling and list-context preservation.
