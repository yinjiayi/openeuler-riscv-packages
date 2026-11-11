<!-- SPDX-License-Identifier: Apache-2.0 -->
# perl-test-tabledriven

This directory packages upstream `https://metacpan.org/dist/Test-TableDriven` version `0.02` for openEuler 24.03 LTS SP3 on `riscv64`/RVA23.

External source and patch licenses remain those of their respective upstream projects. The repository license only covers original packaging metadata, scripts, and documentation.

The fixed official archive is pinned in `sources.yaml`. The original MakeMaker default suite (`t/*.t`) runs unchanged with verbose output; its two files and seven assertions passed host preflight without skips or TODOs. The upstream author-only subdirectory is not selected by the original default harness. No source or test patches are applied.

The copyright and dual Perl-license grant appear in `lib/Test/TableDriven.pm`; `%license` retains that exact upstream file as the license carrier. The short upstream README is documentation, not license evidence.

All eight bundled `inc/Module/Install*` helpers match the fixed official Module::Install 0.67 donor's `inc/` members byte-for-byte, with no normalization. Its original README contains the three authors' copyright and the bundle's dual Perl-license grant; its original LICENSE carries the full terms. Both fixed official text files are SHA-256 pinned in `sources.yaml` and retained as `%license` notices. The donor archive is used only for provenance verification and is not added to the SRPM. No helper or original test is removed or changed.

Installed smoke exercises the real table-driven API with two independent input/output pairs. Host validation does not establish target success: exact-head target build, original tests, actual installation and physical RPM/SRPM must be independently accepted from CI.
