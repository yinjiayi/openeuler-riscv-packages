<!-- SPDX-License-Identifier: Apache-2.0 -->
# Data::Float 0.015

This package maps the frozen Ubuntu `libdata-float-perl` key to the official
[Data-Float 0.015](https://metacpan.org/dist/Data-Float) CPAN release. The
author-directory `CHECKSUMS` and an independent HTTPS download agree on
SHA-256 `8a6cb97aea2f5cfa4fad85d8c39c0ff27822a598626aba4e7f456e0f6d1ff30a`.
The archive is one regular-file/directory tree without traversal paths.
Although CPAN's machine-readable license field says `unknown`, the copyright
holder's included README and the sole installed module's POD explicitly grant
redistribution under Perl's GPL/Artistic choice; no archive file asserts
incompatible terms. CI re-verifies the pinned source before building.

The official openEuler 24.03 LTS SP3 riscv64/RVA23 primary has neither a
`perl-Data-Float` RPM nor a `perl(Data::Float)` provider. It uniquely supplies
the required MakeMaker, Perl core modules, Test::More, Test::Pod and
Test::Pod::Coverage providers. The latter two are hard build dependencies so
the default POD syntax/coverage tests cannot silently skip on target.

All ten upstream default test files remain unchanged. Local macOS passed 719
assertions, with only `t/pod_cvg.t` self-skipping because its optional module
is absent. The upstream suite also has genuine floating-feature conditional
skips; any target-side skip must be reported with its reason. Exact-head CI
must establish the target build, full default test outcome and installed-RPM
functional smoke. PR CI products do not establish public RPM publication.
