<!-- SPDX-License-Identifier: Apache-2.0 -->
# perl-package-variant

This directory packages upstream `https://metacpan.org/dist/Package-Variant` version `1.003002` for openEuler 24.03 LTS SP3 on `riscv64`/RVA23.

The fixed CPAN archive matches the MetaCPAN release digest and the author's
`CHECKSUMS` entry. The original module and generated README grant the same
terms as Perl itself and retain all upstream author and contributor notices.
The maintainer release tag `v1.003002` contains the exact original project
Makefile.PL and maintainer include. The released archive contains `META.yml`;
the original Makefile.PL only evaluates the maintainer-only Distar include
when that file is absent. The recipe requires `META.yml` before configure,
does not bundle Distar and fetches no build dependencies.

The recipe runs the unchanged upstream `make test`, with Moo available so
the parameterized role tests run. The installed smoke test builds two
distinct variants and verifies the parameter-dependent results.

External source and patch licenses remain those of their respective upstream projects. The repository license only covers original packaging metadata, scripts, and documentation.
