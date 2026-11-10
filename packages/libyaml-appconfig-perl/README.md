<!-- SPDX-License-Identifier: Apache-2.0 -->
# libyaml-appconfig-perl

This noarch package provides [YAML::AppConfig](https://metacpan.org/dist/YAML-AppConfig)
0.19 for openEuler 24.03 LTS SP3 on `riscv64`/RVA23. The authorized CPAN
archive is pinned in `sources.yaml`; [Debian stable](https://packages.debian.org/stable/libyaml-appconfig-perl)
establishes the package name. The original complete LICENSE and author notices
are preserved.

The upstream default test suite loads its own helper with relative `do`.
With implicit dot disabled, `%check` supplies the exact verified absolute
source root only to `make test`; all six original files and 244 assertions
remain unmodified. The installed smoke uses the supported YAML backend and
checks interpolation and dump/reload.

External source and patch licenses remain those of their respective upstream projects. The repository license only covers original packaging metadata, scripts, and documentation.
