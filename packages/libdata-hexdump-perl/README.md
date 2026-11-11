<!-- SPDX-License-Identifier: Apache-2.0 -->
# Data::HexDump 0.04

The frozen Ubuntu `libdata-hexdump-perl` key maps to the official
[Data-HexDump 0.04](https://metacpan.org/dist/Data-HexDump) CPAN release. The
publisher's author-directory `CHECKSUMS` and an independent HTTPS download
agree on SHA-256 `bc36f404438ac36ad2b9295539227d36f99cd1623f1e347af77c594c40ccbcf8`.
The ordinary-file archive has one top-level tree and no traversal paths.
Its `LICENSE` names Fabien Tassin and grants Perl's GPL/Artistic terms; the
sole installed module POD independently gives the same grant.

The official openEuler 24.03 LTS SP3 riscv64/RVA23 primary has neither a
`perl-Data-HexDump` RPM nor a `perl(Data::HexDump)` provider. It uniquely
supplies all hard dependencies, including Carp, Exporter, FileHandle, parent
and the core Test module. Both default upstream test files remain unchanged:
local `make test` passes 13 assertions without skips. Exact-head target CI
must prove the full default test suite, target RPM build, installed functional
smoke and physical products. PR CI products do not establish public RPM
publication.
