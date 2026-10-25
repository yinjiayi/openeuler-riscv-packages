<!-- SPDX-License-Identifier: Apache-2.0 -->
# libhash-moreutils-perl

The frozen inventory's `libhash-moreutils-perl` key (Ubuntu source 0.06-2)
maps to official stable [Hash-MoreUtils 0.06](https://metacpan.org/dist/Hash-MoreUtils).
The official HTTPS archive SHA-256 is
`db9a8fb867d50753c380889a5e54075651b5e08c9b3b721cb7220c0883547de8`,
identical to publisher `CHECKSUMS`. The archive contains only regular files
and directories under one root, with no links or traversal paths. Its
README.md, Makefile.PL and META.json consistently declare Perl terms.

The official openEuler 24.03 LTS SP3 `riscv64`/RVA23 `everything` primary
metadata SHA-256 is
`fdb1663ee6c803e8efcc83c19b7a1548f047f08abba8a52f5fe623b222064d1a`.
It contains neither `perl-Hash-MoreUtils` nor `perl(Hash::MoreUtils)`, and
includes all declared build and test dependencies. This is a snapshot
collision check, not a future guarantee.

`%check` retains both default upstream test files (66 assertions passed on
local Perl 5.34.1). The installed-RPM smoke checks its generated module
provider and representative hash-slicing functions. Exact-head target CI
must still establish the SP3 RVA23 RPM build, complete suite and installed
smoke; no local RPM/QEMU result is claimed.
