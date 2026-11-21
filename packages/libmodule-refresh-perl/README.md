<!-- SPDX-License-Identifier: Apache-2.0 -->
# perl-module-refresh

This directory packages upstream `https://metacpan.org/dist/Module-Refresh` version `0.18` for openEuler 24.03 LTS SP3 on `riscv64`/RVA23.

External source and patch licenses remain those of their respective upstream projects. The repository license only covers original packaging metadata, scripts, and documentation.

The source archive is SHA-256 pinned. The original Perl dual-license grant
remains in `Module/Refresh.pm`; both full license texts are independently
pinned from the Perl project. The unmodified MakeMaker default suite covers
reload, cache behavior and removal of obsolete symbols. The installed smoke
test exercises reloading a temporary module with no network or native kernel.
