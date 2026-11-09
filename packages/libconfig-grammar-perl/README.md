<!-- SPDX-License-Identifier: Apache-2.0 -->
# libconfig-grammar-perl

This noarch package provides [Config::Grammar](https://metacpan.org/dist/Config-Grammar)
1.13 for openEuler 24.03 LTS SP3 on `riscv64`/RVA23. The official CPAN
release is pinned in `sources.yaml`, with [Debian stable](https://packages.debian.org/stable/libconfig-grammar-perl)
as naming lineage.

The original distribution LICENSE and module notices are unchanged.
The notice-only patch adds the full original license of the generated
Makefile.PL template from [Dist-Zilla 6.012](https://metacpan.org/release/RJBS/Dist-Zilla-6.012),
SHA-256 `67583075f6d62b78aaa956389f113df789ddd41911394092a5a2b8c6fa863070`.
No original source or test file is changed. Both grants use the same
terms as Perl.

The offline build runs the complete original `make test`, including
dynamic grammars, section inheritance, example parsing and error cases.
The installed smoke loads all three modules and parses an actual file.

External source and patch licenses remain those of their respective upstream projects. The repository license only covers original packaging metadata, scripts, and documentation.
