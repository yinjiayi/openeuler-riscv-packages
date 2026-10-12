<!-- SPDX-License-Identifier: Apache-2.0 -->
# Data::Miscellany 1.100850

The frozen Ubuntu `libdata-miscellany-perl` key maps to the official
[Data-Miscellany 1.100850](https://metacpan.org/dist/Data-Miscellany) CPAN
release. The publisher's author-directory `CHECKSUMS` and an independent HTTPS
download agree on SHA-256 `aacc5fec3cd9d441d9538c3c12d9d9623d228e56828b35daa652143d1b336531`.
The archive has one top-level tree containing ordinary files and directories
only, with no traversal paths. Its `LICENSE` and installed module POD grant
redistribution under the same GPL/Artistic terms as Perl. The module labels
code adapted from Test::More, whose copyright POD grants the same Perl terms;
no bundled file presents a conflicting grant. CI verifies the fixed source.

The official openEuler 24.03 LTS SP3 riscv64/RVA23 primary has neither a
`perl-Data-Miscellany` RPM nor a `perl(Data::Miscellany)` provider. It uniquely
supplies all declared hard dependencies. The complete default upstream suite
remains unchanged: local `make test` passed 43 assertions in three ordinary
files, while 12 author/release-only files self-skipped under upstream's own
default conditions. Exact-head target CI must prove the same default test
behavior, target RPM build and installed functional smoke. PR CI products do
not establish public RPM publication.
