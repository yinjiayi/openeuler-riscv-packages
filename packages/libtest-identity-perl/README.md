<!-- SPDX-License-Identifier: Apache-2.0 -->
# libtest-identity-perl

This package maps the frozen Ubuntu `libtest-identity-perl 0.01-4` lineage
to PEVANS's official CPAN `Test-Identity-0.01.tar.gz` release. The publisher
`CHECKSUMS` and an independent HTTPS download agree on SHA-256
`2f0205009aed152668182aafa16357ab1f47b4cbc001e89871b67387ef8e5f23`.
All source members are regular files or directories beneath one archive root;
there are no links, traversal paths or separately vendored code. The archive
`LICENSE` and installed module grant the same terms as Perl. No upstream VCS
location is declared by this old release; `source_repository` points to the
official MetaCPAN distribution source browser, not a claimed Git repository.

The SHA-256-locked official openEuler 24.03 LTS SP3 RVA23 primary metadata
(`fdb1663ee6c803e8efcc83c19b7a1548f047f08abba8a52f5fe623b222064d1a`)
has neither a same-name RPM nor `perl(Test::Identity)` provider. It supplies
MakeMaker, Scalar::Util, Test::Builder::Module, Test::Builder::Tester,
Test::More and Test::Pod. The upstream archive provides a generated
MakeMaker compatibility entry point as well as Build.PL; the SPEC uses the
unmodified Makefile.PL and retains all three default `t/*.t` files. Pristine
local `make test` passed three files and ten assertions with no skips,
including its POD check. Target DNF and `%check` remain authoritative.

Installed smoke checks RPM ownership/provider and exercises `identical`
with the same reference and with two undefined values. PR CI does not
constitute public repository publication.
