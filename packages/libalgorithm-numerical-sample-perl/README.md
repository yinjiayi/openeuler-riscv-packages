<!-- SPDX-License-Identifier: Apache-2.0 -->
# libalgorithm-numerical-sample-perl

This package maps the frozen inventory's exact
`libalgorithm-numerical-sample-perl` key to the official
[Algorithm-Numerical-Sample 2010011201](https://metacpan.org/dist/Algorithm-Numerical-Sample)
CPAN release. The official CPAN `CHECKSUMS` SHA-256 and an independent HTTPS
download agree on `7253cf258e4be6cc1020ab3ac5d17a9721d67c8cdbf33f1816494dab89f87602`.
The archive has one top-level tree, only regular files and directories, and
no traversal paths. Its README and module POD contain the full MIT license
text; there is no separate LICENSE file. CI verifies the pinned source before
building for openEuler 24.03 LTS SP3 riscv64/RVA23.

The SHA-256-verified official target Everything primary metadata contains
neither a `perl-Algorithm-Numerical-Sample` RPM nor a
`perl(Algorithm::Numerical::Sample)` provider. The target contains the three
optional upstream test dependencies; this package declares them as
BuildRequires to keep the checks active.

Upstream registers four default tests. They primarily verify module loading,
POD, POD coverage, and absence of warnings; they do not measure sampling
fairness. `%check` runs all four unchanged, with Test::Pod,
Test::Pod::Coverage, and Test::NoWarnings installed to avoid their optional
skip paths. The installed-RPM smoke checks finite- and stream-sampling
size, range, uniqueness, and the full-set case. These bounded invariants
do not prove statistical fairness. Local pure-Perl testing lacked
Test::Pod::Coverage and Test::NoWarnings; their target execution must be
confirmed by exact-head CI. PR CI artifacts do not establish public RPM
repository publication.
