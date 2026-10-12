<!-- SPDX-License-Identifier: Apache-2.0 -->
# libalgorithm-loops-perl

This package maps the frozen inventory's exact `libalgorithm-loops-perl`
key to the official [Algorithm-Loops 1.032](https://metacpan.org/dist/Algorithm-Loops)
CPAN release. The official CPAN `CHECKSUMS` SHA-256 and an independent HTTPS
download agree on `437eebed042093b365c1a90c65e53bf9ca2859dd889a0ae845fe9f9da3c6c006`.
The archive has one top-level tree, only regular files and directories,
and no traversal paths. Its included `LICENSE` is the Unlicense public-domain
dedication. CI verifies the pinned source before building for openEuler
24.03 LTS SP3 riscv64/RVA23.

The SHA-256-verified official target Everything primary metadata contains
neither a `perl-Algorithm-Loops` RPM nor a `perl(Algorithm::Loops)` provider.
This target check is distinct from the frozen inventory's external Ubuntu
discovery record.

Upstream registers two default test files, `t/assert.t` and `t/basic.t`.
`%check` runs both unchanged (111 assertions). The installed-RPM smoke checks
the version and element-transforming, mapping, and numeric permutation functions.
Local pure-Perl tests passed on macOS, but only exact-head CI can establish
the target RPM/QEMU result. PR CI artifacts do not establish public RPM
repository publication.
