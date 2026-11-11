<!-- SPDX-License-Identifier: Apache-2.0 -->
# libclass-meta-perl

This directory packages upstream `https://metacpan.org/dist/Class-Meta` version `0.66` for openEuler 24.03 LTS SP3 on `riscv64`/RVA23.

External source and patch licenses remain those of their respective upstream projects. The repository license only covers original packaging metadata, scripts, and documentation.

The exact official CPAN release SHA-256 is
`d945edeb653a184f28caa22702e49ceea92ae839b722e49cab4ab1150df4598b`.
It matches both the authorized release index and the signed CPAN author
`CHECKSUMS`. Debian stable version 0.66-3 establishes naming lineage only.

The original archive and README preserve David E. Wheeler's grant under the
same terms as Perl itself. The archived `Makefile.PL` identifies the
`Module::Build::Compat` 0.40 traditional template. The exact official
Module-Build 0.40 donor archive SHA-256 is
`230025eafb75ae8aa513db228af150f223d6d73bda4989b7ffcc80cebff984c0`.
The donor archive is not repackaged; the original generated file is unchanged,
the corresponding Ken Williams notice is shipped, and both full Perl license
texts come from the fixed official Perl 5.38.0 commit.

Build and test use the original MakeMaker entry point and default tests,
including both POD checks. With newer Data::Types the upstream suite itself
skips six old assertions that expected zero to be rejected as a whole number.
Those tests are unchanged. The separate installed smoke checks the current
behavior by creating a typed accessor and round-tripping zero.
