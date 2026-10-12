<!-- SPDX-License-Identifier: Apache-2.0 -->
# libtest-version-perl

The frozen inventory records Debian `libtest-version-perl 2.09-2` and Fedora
`perl-Test-Version 2.09` lineage. This package uses the official PLICEASE CPAN
`Test-Version-2.09.tar.gz` release. The publisher's `CHECKSUMS` and an
independent HTTPS download agree on SHA-256
`9ce1dd2897a5f30e1b7f8966ec66f57d8d8f280f605f28c7ca221fa79aca38e0`.
The 90 archive entries are regular files/directories under one root, with no
links or traversal paths. Its complete `LICENSE`, README, metadata, and
installed module grant Artistic-2.0; the `corpus/` files are test fixtures,
not separately vendored libraries or installed modules.

The SHA-256-locked official openEuler 24.03 LTS SP3 RVA23 primary metadata
(`fdb1663ee6c803e8efcc83c19b7a1548f047f08abba8a52f5fe623b222064d1a`)
has no `perl-Test-Version` RPM or `perl(Test::Version)` provider. It has the
required File::Find::Rule::Perl 1.16, Module::Metadata 1.000038, Test::Simple
1.302198, Test::Exception 0.43, version 0.9930, and their direct provider
dependencies. DNF in exact-head CI must still prove the target transaction.

All 21 unmodified default upstream `t/*.t` files run through `make test`.
Upstream `t/mswin32.t` explicitly self-skips on non-Windows systems; the other
20 default files must pass. The local macOS host lacks
`File::Find::Rule::Perl`, so no local full-suite pass is claimed. The target
build is the authority for original test counts and any further skip. The
installed smoke checks RPM ownership and runs `version_ok` against the
installed module. PR CI success does not mean public repository publication.
