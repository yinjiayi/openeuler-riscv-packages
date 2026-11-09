<!-- SPDX-License-Identifier: Apache-2.0 -->
# libstatistics-linefit-perl

`Statistics::LineFit` fits a straight line to weighted or unweighted data and
reports the fitted coefficients and diagnostics. This noarch package uses the
official [CPAN release](https://metacpan.org/dist/Statistics-LineFit) 0.07 for
openEuler 24.03 LTS SP3 on `riscv64`/RVA23.

[Debian stable](https://packages.debian.org/stable/libstatistics-linefit-perl)
supplies discovery lineage; `sources.yaml` pins the exact upstream archive by
SHA-256. The original `LICENSE` is retained. The archive expands into the
unversioned `Statistics-LineFit` directory. No source patch is needed.
The archive and RPM are version 0.07, but the shipped Perl module declares
`$VERSION = 0.06`. This package preserves that upstream declaration; it does
not satisfy a module-version requirement of `Statistics::LineFit >= 0.07`.

The package builds offline. `%check` runs the full original `make test` suite,
including its 100,000-point numerical test. Installed smoke verifies the
RPM and module versions separately, checks for the method added in release
0.07, and fits three points with known slope and intercept.

External source and patch licenses remain those of their respective upstream projects. The repository license only covers original packaging metadata, scripts, and documentation.
