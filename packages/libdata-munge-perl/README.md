<!-- SPDX-License-Identifier: Apache-2.0 -->
# Data::Munge 0.111

This package maps the frozen Ubuntu `libdata-munge-perl` key to the official
[Data-Munge 0.111](https://metacpan.org/dist/Data-Munge) CPAN release. The
publisher's author-directory `CHECKSUMS` and an independent HTTPS download
agree on SHA-256 `086face7ee925d49782a0dc6c699d27e1ac3c5cc6dfc6e99d3e7d892d2038d9b`.
The archive has one top-level tree, regular files/directories only and no
traversal paths. The copyright holder's included README and sole installed
module POD explicitly grant GPL/Artistic redistribution, with no conflicting
file-level terms. CI re-verifies these pinned source bytes before building.

The official openEuler 24.03 LTS SP3 riscv64/RVA23 primary has neither a
`perl-Data-Munge` RPM nor a `perl(Data::Munge)` provider. It uniquely supplies
MakeMaker, Test2::V0, Test::Pod, Test::Harness, Exporter and Scalar::Util.
The latter is an explicit runtime dependency because an exported function
loads it dynamically.

All four default upstream `t/` files remain unchanged and passed locally
with 89 assertions and no skips. The separate upstream `xt/pod.t` author test
passed one local assertion and is also included in target `%check`. Exact-head
CI must establish target build, test outcomes and installed-RPM functional
smoke; PR products do not prove public RPM publication.
