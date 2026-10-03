# Data::Censor 0.04

The frozen 2026-08-08 inventory includes Fedora Everything-source
`perl-Data-Censor` 0.04-3.fc44. This package uses the official BIGPRESH CPAN
0.04 tarball, SHA-256
`b713694b004362ba799baca9ee96a5d1c45a5e297711e3312f741ef511e2cc83`,
matching the publisher's `CHECKSUMS`. Official openEuler 24.03-LTS-SP3
riscv64 RVA23 primary metadata has no same RPM or `perl(Data::Censor)`
provider. It supplies Ref::Util 0.204 and its XS dependency, Clone 0.46,
Test::Pod 1.52, Test::More and build tools.

The archive has no separate LICENSE file. Its README and only installed PM,
both by David Precious, explicitly grant **this program** under Artistic
License 2.0. The PM says its Dancer-origin code was originally written by
that same author. No contrary notice appears in the four tests, build files
or metadata. `META.json` says `unknown`; it is not our grant evidence. This
rights conclusion is limited to the publisher's checksum-verified archive.

All four original default test files are unchanged. `t/manifest.t` is an
upstream `RELEASE_TESTING`-only metadata check that self-skips by default.
The other three files must run 15 assertions in target `%check`; `Clone` is a
hard build/runtime dependency so the four clone assertions cannot silently
skip. Local macOS lacks Ref::Util, so no local upstream suite result is
claimed. Exact-head hosted CI must prove the target suite and installed
smoke; this PR does not merge or publish the package.
