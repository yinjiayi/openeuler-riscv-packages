<!-- SPDX-License-Identifier: Apache-2.0 -->
# libscalar-util-numeric-perl

This architecture-specific package provides [Scalar::Util::Numeric](https://metacpan.org/dist/Scalar-Util-Numeric)
0.40 for openEuler 24.03 LTS SP3 on `riscv64`/RVA23. The authorized CPAN
source is pinned in `sources.yaml`; [Debian stable](https://packages.debian.org/stable/libscalar-util-numeric-perl)
establishes naming lineage. The upstream README and bundled Devel::PPPort
header are retained unmodified for their original grants and attributions.

The recipe requires the actual XS object and runs the complete default
`make test` unchanged. The original POD test points at `../blib` from
the source root; a separate check therefore validates the actual module
under `blib`. Installed smoke loads the XS object and exercises integer,
decimal and invalid-string predicates.

External source and patch licenses remain those of their respective upstream projects. The repository license only covers original packaging metadata, scripts, and documentation.
