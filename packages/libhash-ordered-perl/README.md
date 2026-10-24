<!-- SPDX-License-Identifier: Apache-2.0 -->
# libhash-ordered-perl

The frozen inventory's `libhash-ordered-perl` key (Ubuntu source 0.014-2)
maps to official stable [Hash-Ordered 0.014](https://metacpan.org/dist/Hash-Ordered).
The official HTTPS archive SHA-256 is
`8dc36cd79155ae37ab8a3de5fd9120ffba9a31e409258c28529ec5251c59747b`,
identical to publisher `CHECKSUMS`. All archive entries are regular files or
directories under one root, with no links or traversal paths. Its bundled
LICENSE, README, module, Makefile.PL and META.json agree on Apache-2.0.

The official openEuler 24.03 LTS SP3 `riscv64`/RVA23 `everything` primary
metadata SHA-256 is
`fdb1663ee6c803e8efcc83c19b7a1548f047f08abba8a52f5fe623b222064d1a`.
It contains neither `perl-Hash-Ordered` nor `perl(Hash::Ordered)`, and
includes all declared build/test dependencies and core runtime providers.
This is a snapshot collision check, not a future guarantee.

`%check` retains all four default upstream test files (112 assertions passed
on local Perl 5.34.1). Local Test::FailWarnings 0.008 was installed only in a
temporary test prefix from a SHA-256-verified official CPAN archive; the
target SP3 repository already provides it. The installed-RPM smoke checks
the module provider and ordered-hash API. Exact-head target CI must still
establish the SP3 RVA23 RPM build, complete suite and installed smoke; no
local RPM/QEMU result is claimed.
