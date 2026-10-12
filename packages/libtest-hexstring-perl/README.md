<!-- SPDX-License-Identifier: Apache-2.0 -->
# libtest-hexstring-perl

This package maps the frozen Ubuntu `libtest-hexstring-perl 0.03-2` lineage
to PEVANS's official CPAN `Test-HexString-0.03.tar.gz` release. The publisher
`CHECKSUMS` and an independent HTTPS download agree on SHA-256
`7d4c4cdc192f2594dc78ff75eb2cf4d0561f794b36ee0eacee8c4a1aa8a03f40`.
All archive members are regular files or directories beneath one root; there
are no links, traversal paths or separately vendored code. The archive
`LICENSE` and installed module grant the same terms as Perl. No upstream VCS
location is declared by this release, so the metadata points to the official
MetaCPAN distribution source browser rather than inventing a Git repository.

The SHA-256-locked official openEuler 24.03 LTS SP3 RVA23 primary metadata
(`fdb1663ee6c803e8efcc83c19b7a1548f047f08abba8a52f5fe623b222064d1a`)
has neither a same-name RPM nor `perl(Test::HexString)` provider. It supplies
the direct dependencies, including Test::Builder, Test::Builder::Tester,
Test::More and Test::Pod. Exact-head DNF must still prove target closure.

The upstream archive includes a generated MakeMaker compatibility entry point
alongside Build.PL. The SPEC uses that unmodified Makefile.PL and keeps all
three original default `t/*.t` files in `%check`. Pristine local `make test`
passed three files and seven assertions with no skips, including POD. Its
negative and diagnostic cases remain in the original suite; installed smoke
checks packaged `is_hexstr` on binary and text inputs plus RPM ownership.
PR CI is not public repository publication.
