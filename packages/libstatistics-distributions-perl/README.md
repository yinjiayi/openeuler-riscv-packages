<!-- SPDX-License-Identifier: Apache-2.0 -->
# libstatistics-distributions-perl

`Statistics::Distributions` calculates probabilities and quantiles for common
statistical distributions in Perl. This noarch package uses the official
[CPAN release](https://metacpan.org/dist/Statistics-Distributions) 1.02 for
openEuler 24.03 LTS SP3 on `riscv64`/RVA23. The exact SHA-256 is pinned in
`sources.yaml`; [Debian stable](https://packages.debian.org/stable/libstatistics-distributions-perl)
provides discovery lineage.

The upstream tarball has no separate license file. The package installs a
verbatim copy of the module's copyright and permission section, which states
the same terms as Perl itself, and retains the original module documentation.
No source patch is required.

The offline build runs the original `make test` and uses `prove` to enforce
the original TAP plan (the test's declared assertion count). It ships the
generated `autosplit.ix` index, which MakeMaker creates alongside the module.
Installed smoke verifies that index, the module version, and known normal and
chi-square quantiles.

External source and patch licenses remain those of their respective upstream projects. The repository license only covers original packaging metadata, scripts, and documentation.
