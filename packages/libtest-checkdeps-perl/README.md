<!-- SPDX-License-Identifier: Apache-2.0 -->
# libtest-checkdeps-perl

This package maps the frozen Ubuntu `libtest-checkdeps-perl 0.010-6`
lineage to LEONT's official CPAN `Test-CheckDeps-0.010.tar.gz` release.
The official publisher `CHECKSUMS` and an independent HTTPS download agree
on SHA-256
`66fccca6c6f330e7ecc898bd6a51846e2145b3e02d78c4997ba6b7de23b551ee`.
The top-level `LICENSE` and installed `Test::CheckDeps` module grant the
same terms as Perl. The distribution contains no separately vendored code.

The SHA-256-locked official openEuler 24.03 LTS SP3 RVA23 primary metadata
(`fdb1663ee6c803e8efcc83c19b7a1548f047f08abba8a52f5fe623b222064d1a`)
has neither a same-name RPM nor `perl(Test::CheckDeps)` provider. It supplies
the direct configure, runtime and default-test prerequisites, including
CPAN::Meta, CPAN::Meta::Check and Test::More. Exact-head DNF installation is
still required to prove target closure.

All four default upstream `t/*.t` files remain in `%check`. A pristine
local `make test` passed 14 assertions, while two `release-*` POD files
self-skipped because the upstream `RELEASE_TESTING` switch was not set. They
are release-candidate checks, not completed default POD coverage; this
package does not claim they ran. Installed smoke constructs an in-memory
CPAN::Meta fixture and verifies `check_dependencies_opts` checks a present
Test::Builder requirement, along with RPM provider and file ownership.
PR CI is not public repository publication.
