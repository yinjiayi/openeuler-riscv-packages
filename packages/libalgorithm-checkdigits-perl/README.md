<!-- SPDX-License-Identifier: Apache-2.0 -->
# libalgorithm-checkdigits-perl

This package maps the frozen inventory's `libalgorithm-checkdigits-perl`
lineage (Debian 1.3.6-2) to the official [Algorithm-CheckDigits 1.3.6
release](https://metacpan.org/dist/Algorithm-CheckDigits). The official CPAN
`CHECKSUMS` file and an independent HTTPS archive download agree on SHA-256
`0f2487a8fd1f31b19c51b2650842f2264c1e77d962487a13b521bbe066c4b4bc`.
The archive has 83 regular files/directories under one root, no links or
traversal paths, and no bundled third-party code. The distribution README,
primary module and installed command grant use under the same terms as Perl.
The source archive also contains a CGI example, which is not installed.

The SHA-256-locked official openEuler 24.03 LTS SP3 `riscv64`/RVA23 primary
metadata has no `perl-Algorithm-CheckDigits` RPM or
`perl(Algorithm::CheckDigits)` provider. It has the Perl, Module::Build,
Pod::Usage, Getopt::Long, version, Test::More, Test::Pod and
Test::Pod::Coverage dependencies. `Probe::Perl` is **not** in that official
repository; it was independently verified as `perl-Probe-Perl 0.03-1` with
`perl(Probe::Perl)` in the then-current public supplemental immutable
generation's state-bound metadata, and its downloaded RPM bytes matched the
metadata checksum. A later repository state may differ; exact-head CI must
prove DNF can install this prerequisite rather than infer it from main.

All 19 upstream default `t/*.t` files are retained in `%check`. In a pristine
local source test, 683 assertions passed. `t/94-version.t` self-skipped because
optional `Test::Version` is not available, and `t/pod-coverage.t` self-skipped
because the local host lacks `Test::Pod::Coverage`; neither skip is a pass.
The target official repository has `Test::Pod::Coverage`, which the SPEC
requires so target CI must actually run that file. The installed smoke checks
valid and invalid IMEI behavior through both the module and the packaged
command. This package is not publicly available merely because PR CI passes.
