<!-- SPDX-License-Identifier: Apache-2.0 -->
# libtest-hasversion-perl

This package maps the frozen Ubuntu `libtest-hasversion-perl 0.014-3` lineage
to FERREIRA's official CPAN `Test-HasVersion-0.014.tar.gz` release. The
publisher `CHECKSUMS`, MetaCPAN release metadata and an independent HTTPS
download agree on SHA-256
`0555bb7ac67d839747056054669065e1305ff4b4e7283d9ac43b7a62cd007cbd`.
All 29 archive entries are regular files/directories under one root, with no
links or traversal paths. The archive-wide `LICENSE` and installed module
grant the same terms as Perl; the CLI and test fixtures are part of that
distribution, with no separately vendored implementation.

The SHA-256-locked official openEuler 24.03 LTS SP3 RVA23 primary metadata
(`fdb1663ee6c803e8efcc83c19b7a1548f047f08abba8a52f5fe623b222064d1a`)
has neither a same-name RPM nor `perl(Test::HasVersion)` provider. It supplies
the runtime/test prerequisites, including Test::Builder::Tester 1.302198,
Test::Pod 1.52 and Test::Pod::Coverage 1.10. Exact-head CI must prove DNF
closure and installation rather than infer it from metadata alone.

All eight default upstream `t/*.t` files remain in `%check`. A pristine
local test passed 20 assertions; `t/98_pod-coverage.t` self-skipped because
the macOS host lacks Test::Pod::Coverage. The target SPEC requires that
official provider, so target CI must run this default coverage file. The
installed smoke exercises the packaged `test_version` command against the
installed module, in addition to RPM ownership/provider checks. PR CI
success is not public repository publication.
