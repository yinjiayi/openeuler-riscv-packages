<!-- SPDX-License-Identifier: Apache-2.0 -->
# libmodule-find-perl

This directory packages [Module::Find 0.17](https://metacpan.org/release/CRENZ/Module-Find-0.17) for openEuler 24.03 LTS SP3 on `riscv64`/RVA23 as `perl-module-find`. The frozen Ubuntu package name is lineage evidence only.

The CPAN archive is unmodified and SHA-256 pinned. The build uses all 15 original default tests, including META validation, POD, coverage, taint mode and symlink behavior. The installed smoke test discovers both a direct child and a nested child in an isolated namespace and loads the direct child. Use module-loading helpers only with trusted search directories.

Module::Find retains Christian Renz's grant under the same terms as Perl. Its `Makefile.PL` incorporates the build-only GPL-3.0-only `WriteMakefile1` helper from Alexandr Ciornii's App-EUMM-Upgrade 0.21. The combined license field accounts for both parts of the source archive; the helper is not installed in `Module/Find.pm`. The RPM includes the original notice, helper attribution and the complete pinned license texts.

External source and patch licenses remain those of their respective upstream projects. The repository license only covers original packaging metadata, scripts, and documentation.
