# Algorithm::Annotate 0.10

Official source: `https://cpan.metacpan.org/authors/id/C/CL/CLKAO/Algorithm-Annotate-0.10.tar.gz`.
The publisher `CHECKSUMS` in the same directory records SHA-256
`c9b1764643933eb1a3356906cc372d483a99416207a31df3e58ee9892d9922f9`.
The archive has one safe root, only regular files/directories, and no patches.

The official `Annotate.pm` POD identifies copyright holder Chia-liang Kao and
explicitly grants redistribution and modification under Perl's terms. The RPM
maps this to `GPL-1.0-or-later OR Artistic-1.0-Perl` and installs that module
source as its license notice. The archive has no separate README or LICENSE.

The official openEuler 24.03-LTS-SP3 riscv64 RVA23 primary has no
`perl-Algorithm-Annotate` name or `perl(Algorithm::Annotate)` provider. It
uniquely supplies `perl(Algorithm::Diff) = 1.201` from `perl-Algorithm-Diff`
Epoch 1, exceeding the upstream 1.15 prerequisite, plus all declared build
tools and `perl(Test::More)`. No fallback or test patch is used.

The complete default upstream `t/1basic.t` passes locally (one file, three
assertions, no skips), including a repeat using checksum-verified official
Algorithm::Diff 1.201. Target CI must still prove the exact-head RPM build,
full `%check`, and installed functional smoke before target success is claimed.

Frozen Fedora `0.10-53.fc44` row is discovery lineage, not source,
licensing, dependency, or target-build proof.
