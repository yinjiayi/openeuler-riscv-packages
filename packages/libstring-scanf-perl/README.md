<!-- SPDX-License-Identifier: Apache-2.0 -->
# libstring-scanf-perl

The frozen inventory's exact `libstring-scanf-perl` key maps to the official
stable [String-Scanf 2.1](https://metacpan.org/dist/String-Scanf) CPAN release.
Its official HTTPS archive SHA-256 is
`c519f6bf7c54f92a72a05f317c730f4fd450945672947782fb4e17b9c1176837`,
identical to the publisher's `CHECKSUMS` entry. All 11 archive entries are
regular files or directories within one root, without traversal paths or
links. The module's `AUTHOR, COPYRIGHT AND LICENSE` POD grants the same terms
as Perl itself. CPAN META leaves license unspecified rather than asserting
conflicting terms. The SPEC installs the module source as a license document
because this release has no separate license file.

The official openEuler 24.03 LTS SP3 `riscv64`/RVA23 `everything` primary
metadata SHA-256 is
`fdb1663ee6c803e8efcc83c19b7a1548f047f08abba8a52f5fe623b222064d1a`.
It contains neither `perl-String-Scanf` nor a `perl(String::Scanf)` provider
and includes the declared Perl build tools. This is a snapshot check, not a
future guarantee.

`%check` retains the complete default upstream test file, `t/scanf.t` (135
assertions passed on local Perl 5.34.1). The installed-RPM smoke checks
module version plus function and object parsing. Exact-head target CI must
still establish the SP3 RVA23 RPM build, full suite, and installed smoke;
none is claimed from the local Perl run.
