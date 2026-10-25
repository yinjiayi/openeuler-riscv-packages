<!-- SPDX-License-Identifier: Apache-2.0 -->
# perl-string-ttylength

The frozen inventory contains `perl-string-ttylength` 0.03-1 from AUR and
`perl-String-TtyLength` 0.03-15.fc44 from Fedora Everything-source. The
official [String-TtyLength 0.03](https://metacpan.org/dist/String-TtyLength)
CPAN tarball is 10,967 bytes with SHA-256
`4fedaf72028511d80eb6afba523993e9aaa245d7af558345d5d4ed46e2e82ce1`,
matching NEILB's publisher `CHECKSUMS`. Its archive is a single rooted tree
of regular files and directories, with no links, special files, vendored
code or third-party data. The distribution-wide `LICENSE` and module POD
grant the same terms as Perl 5; the explicit GPL-1.0-or-later path is used
in RPM metadata. The separate Artistic option is not assigned an inferred
version here. The license text is installed with the RPM.

The official openEuler 24.03 LTS SP3 RVA23 primary metadata (SHA-256
`fdb1663ee6c803e8efcc83c19b7a1548f047f08abba8a52f5fe623b222064d1a`)
has no `perl-String-TtyLength` or `perl(String::TtyLength)` provider. It does
provide `perl(Unicode::EastAsianWidth) = 12.0` from
`perl-Unicode-EastAsianWidth-12.0-2.oe2403sp3` and `perl(Test2::V0)` for
the original tests. Those are snapshot checks, not guarantees about later
repository state.

Both original upstream test files remain unchanged: 13 ANSI/length cases
and five Unicode/width cases. A local source-only run passed all 18 using
the separately SHA-256-verified official Unicode::EastAsianWidth 12.0 Perl
module because that dependency is absent on the local macOS host. This is
not an RPM or RISC-V build. Target CI must run the unchanged `%check` and
then install the resulting RPM; installed smoke checks the RPM provider,
ANSI stripping, ASCII, CJK and emoji widths. These are functional checks,
not a claim about terminal font rendering or native RISC-V performance.
A successful PR build is not evidence of public repository publication.
