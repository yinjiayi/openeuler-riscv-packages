<!-- SPDX-License-Identifier: Apache-2.0 -->
# libmath-nocarry-perl

The frozen discovery snapshot records Math::NoCarry 1.117 in Ubuntu and
Debian. This package uses the official stable [Math-NoCarry 1.117](https://metacpan.org/dist/Math-NoCarry)
CPAN release. The source SHA-256 is
`599cf98b030befe2fbf00ce5746cc1776b6e7f0fe6af9b61c7b3dae94ffee78a`,
matching the publisher's `B/BR/BRIANDFOY/CHECKSUMS` and an independent HTTPS
download. The archive has one root, 26 regular-file/directory entries, no
links, special files or traversal paths.

The included `LICENSE` explicitly grants Artistic License 2.0. The installed
`lib/Math/NoCarry.pm` POD states the same grant, and release metadata declares
`artistic_2`. No file introduces a conflicting per-file license. The RPM
license is `Artistic-2.0`.

Official openEuler 24.03 LTS SP3 RVA23 primary metadata (SHA-256
`fdb1663ee6c803e8efcc83c19b7a1548f047f08abba8a52f5fe623b222064d1a`)
has neither `perl-Math-NoCarry` nor `perl(Math::NoCarry)`. It contains
`perl-version` 0.99.30 (providing `perl(version)`, above the upstream 0.86
minimum), `perl-ExtUtils-MakeMaker` 7.70 (above 6.64), `perl-Test-Simple`,
`perl-Test-Pod` 1.52, `perl-Test-Pod-Coverage` 1.10 and `perl-generators`.
Build requirements include the optional POD testing packages so both POD
tests run instead of skipping. `Test::Manifest` is an optional configure-time
helper unavailable in this target repository; the generated `make test` still
executes every default `t/*.t` file listed in `t/test_manifest`.

The complete upstream default suite consists of `add.t`, `load.t`,
`multiply.t`, `pod.t`, `pod_coverage.t`, and `subtract.t`. The separate
`xt/changes.t` is a release-author test and is not part of upstream's default
`make test`; it requires `Test::CPAN::Changes`, which is absent from the target
repository. `%check` preserves unmodified `make test`, including all six
default files. The installed smoke checks the RPM/provider, module version and
no-carry add, subtract and multiply behavior. Its inputs use writable Perl
variables because upstream's arithmetic functions coerce their arguments in
place; read-only literal arguments would produce a Perl error unrelated to
installed packaging. Target build, default tests and smoke need exact-head
hosted CI evidence. PR CI does not prove public repository publication.
