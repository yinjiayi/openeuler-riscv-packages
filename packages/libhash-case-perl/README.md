<!-- SPDX-License-Identifier: Apache-2.0 -->
# libhash-case-perl

The frozen inventory's `libhash-case-perl` key (Ubuntu source 1.070-1)
maps to official stable [Hash-Case 1.07](https://metacpan.org/dist/Hash-Case).
The official HTTPS archive SHA-256 is
`f591db9f9a8355c67fba94ae27e06e6339b800ca78c5250d75c7688c0bc33969`,
identical to publisher `CHECKSUMS`. The archive contains only regular files
and directories under one root, with no links or traversal paths. Its
README.md, module SPDX header, Makefile.PL and META.json consistently state
the same terms as Perl itself.

The official openEuler 24.03 LTS SP3 `riscv64`/RVA23 `everything` primary
metadata SHA-256 is
`fdb1663ee6c803e8efcc83c19b7a1548f047f08abba8a52f5fe623b222064d1a`.
It contains neither `perl-Hash-Case` nor providers for any of the four
`Hash::Case` modules. Its declared build and test dependencies and Perl core
runtime providers are present. This is a snapshot collision check, not a
future guarantee.

`%check` retains all four default upstream test files (140 assertions passed
on local Perl 5.34.1). The installed-RPM smoke checks the module provider and
lower-, upper- and preserved-case tied hashes. Exact-head target CI must still
establish the SP3 RVA23 RPM build, complete suite and installed smoke; no
local RPM/QEMU result is claimed.
