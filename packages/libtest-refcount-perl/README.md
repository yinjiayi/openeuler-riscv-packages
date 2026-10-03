<!-- SPDX-License-Identifier: Apache-2.0 -->
# libtest-refcount-perl

This package maps the frozen Ubuntu `libtest-refcount-perl 0.10-4` lineage
to PEVANS's official CPAN `Test-Refcount-0.10.tar.gz` release. The publisher
`CHECKSUMS` and an independent HTTPS download agree on SHA-256
`0457c20a4956473d157c4faaff8814154bc93f6e2b543c2812a19ff8e3370eb2`.
All archive members are regular files or directories beneath one root, with
no links or separately vendored code. The archive `LICENSE`, module header
and Build.PL grant the same terms as Perl; the tests, metadata and documents
carry no conflicting rights notice. The release declares no upstream VCS
location, so metadata uses its official MetaCPAN source browser.

The SHA-256-locked official openEuler 24.03 LTS SP3 RVA23 primary metadata
(`fdb1663ee6c803e8efcc83c19b7a1548f047f08abba8a52f5fe623b222064d1a`)
contains neither a same-name RPM nor `perl(Test::Refcount)` provider. It
supplies the declared B, Scalar::Util, Test::Builder, Module::Build and
Test::More/Test::Builder::Tester prerequisites, plus Test::Pod for the
upstream default POD file. Target DNF remains the final closure check.

The SPEC uses unmodified Build.PL and keeps all six original default
`t/*.t` files in `%check`. Pristine local `./Build test` passed 21 planned
assertions; one regexp-reference case was explicitly self-skipped by the
unchanged upstream Perl-version condition (`Bleadperl`). The optional
recommended Devel::MAT diagnostic dumper was absent locally, but core
reference-count tests executed; no XS or native feature was substituted.
Installed smoke checks both one- and two-reference assertions and RPM
ownership. Pull-request CI is not public repository publication.
