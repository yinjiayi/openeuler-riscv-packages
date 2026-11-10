<!-- SPDX-License-Identifier: Apache-2.0 -->
# libmodule-manifest-perl

This directory packages upstream `https://metacpan.org/dist/Module-Manifest` version `1.09` for openEuler 24.03 LTS SP3 on `riscv64`/RVA23.

The authorized CPAN archive is pinned in `sources.yaml` and matches the
publisher CHECKSUMS and MetaCPAN release metadata. The full original
same-Perl LICENSE is retained. Debian stable 1.09-2 establishes lineage;
no Debian build recipe is run or copied.

The noarch recipe uses upstream MakeMaker, and runs all four original
default test files. Upstream's stock suite plans 34 TAP cases, with five
explicit skips because no MANIFEST.SKIP is shipped. A second run of the
unchanged suite uses a temporary positive fixture to exercise all 34.
The fixture is not packaged. Installed smoke checks manifest parsing and
exclusion matching without requiring extra modules.

External source and patch licenses remain those of their respective upstream projects. The repository license only covers original packaging metadata, scripts, and documentation.
