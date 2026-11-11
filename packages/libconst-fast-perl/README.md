<!-- SPDX-License-Identifier: Apache-2.0 -->
# libconst-fast-perl

This directory packages [Const::Fast 0.014](https://metacpan.org/release/LEONT/Const-Fast-0.014) for openEuler 24.03 LTS SP3 on `riscv64`/RVA23. It uses the original CPAN archive and bundled author license; the AUR and Ubuntu catalog records provide naming lineage only.

The package retains the upstream Module::Build::Tiny default test action. It dispatches all four shipped test files; two POD files skip under upstream's own release-only condition. The installed smoke test exercises read-only scalar behavior. No source patch is used.

External source and patch licenses remain those of their respective upstream projects. The repository license only covers original packaging metadata, scripts, and documentation.
