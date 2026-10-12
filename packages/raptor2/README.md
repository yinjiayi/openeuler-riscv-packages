<!-- SPDX-License-Identifier: Apache-2.0 -->
# raptor2

This directory packages upstream Raptor `2.0.16` for openEuler 24.03 LTS
SP3 on `riscv64`/RVA23. `raptor2` is the canonical RPM ID and the package
keeps the upstream `libraptor2.so.0` ABI while upgrading the target repository
from `2.0.15-21.oe2403sp3` to `2.0.16-1`.

The frozen snapshot `discovery-20260808T165000Z-9a89920c269462cd`
cross-checks Arch Extra `raptor` `2.0.16-9`, AUR metadata-only
`lib32-raptor` `2.0.16-3`, Fedora 44 `raptor2` `2.0.15-50.fc44`, Debian
stable `raptor2` `2.0.16-6`, openSUSE Tumbleweed `raptor` `2.0.16-5.8`, and
Ubuntu Resolute `raptor2` `2.0.16-6build1`. No external packaging recipe was
read as executable content or executed.

The official upstream release tarball is pinned at SHA-256
`089db78d7ac982354bdbf39d973baf09581e6904ac4c92a98c5caadb3de44680`.
It is a single-root archive with no unsafe paths, links, or special files and
contains the complete unit, parser, serializer, expected-failure, RDF/XML,
Turtle, TriG, N-Triples, N-Quads, RDFa, JSON, GRDDL, and feed fixture suites.
All parsers and serializers are enabled and `%check` runs upstream `make
check` unchanged. The build stage has no network; the WWW unit's attempted
fetch is therefore denied by the CI network boundary without removing or
skipping that upstream test target.

External source licenses remain those of upstream. The repository's
Apache-2.0 license covers only the original packaging metadata, scripts, and
documentation in this directory.
