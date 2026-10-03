<!-- SPDX-License-Identifier: Apache-2.0 -->
# libtest-fixme-perl

The frozen Ubuntu `libtest-fixme-perl 0.17-1` and Fedora
`perl-Test-Fixme 0.17-3.fc44` lineages map to PLICEASE's official CPAN
`Test-Fixme-0.17.tar.gz`. Its SHA-256
`9ef8580420b0551f11e81541a22006837c9bdf26524d0b8bf35aa286acca878e`
matches the publisher's `CHECKSUMS`. The archive has one root and no
separately vendored source. Its distribution-wide `LICENSE` states that
"This software" is licensed as Perl 5, with explicit GPL-1-or-later and
Artistic License alternatives. The module and distribution metadata agree;
test and fixture files carry no conflicting notice.

The SHA-256-locked official openEuler 24.03 LTS SP3 RVA23 primary metadata
(`fdb1663ee6c803e8efcc83c19b7a1548f047f08abba8a52f5fe623b222064d1a`)
contains neither a same-name RPM nor `perl(Test::Fixme)` provider. It
provides the module's core dependencies and default-test modules, including
ExtUtils::Manifest, Test::Builder, Test::More and File::Temp. Exact-head DNF
must still prove target closure.

The SPEC uses unmodified upstream Makefile.PL and retains all ten original
`t/*.t` files in `%check`. Pristine local `make test` passed 94 assertions;
`t/skip_all.t` deliberately self-skipped and is not counted as a passing
test. The separate `xt/author` and `xt/release` suites are not default tests.
Installed smoke checks RPM ownership, a passing `run_tests` scan and direct
FIXME-marker detection. Pull-request CI is not public repository publication.
