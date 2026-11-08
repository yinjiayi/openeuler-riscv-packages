<!-- SPDX-License-Identifier: Apache-2.0 -->
# libtext-mediawikiformat-perl

The frozen inventory's Ubuntu source `libtext-mediawikiformat-perl` 1.04-3
maps to the official stable CPAN Text-MediawikiFormat 1.04 release. Its HTTPS
archive SHA-256 `435c3da5618259d4dc79b7b21ef095bcf2771628306824af0831387c342f26d7`
matches the publisher's `CHECKSUMS` entry. The archive has one root, regular
files and directories only, and no traversal paths.

The README and main module POD grant the same terms as Perl; the two companion
module POD notices specify Perl 5.8.x terms. The distribution declares
`perl_5` in `META.json` and ships the Artistic and GPL version 2 license
texts. The RPM records the common GPL-2.0-only or Artistic-1.0-Perl choice;
it does not infer a later GPL version from the bundled GPL text.

The official openEuler 24.03 LTS SP3 `riscv64` RVA23 primary metadata
(SHA-256 `fdb1663ee6c803e8efcc83c19b7a1548f047f08abba8a52f5fe623b222064d1a`)
has no `perl-Text-MediawikiFormat` RPM or `perl(Text::MediawikiFormat)`
provider. It does provide the declared runtime and test modules, including
CGI, URI, HTML::Parser, HTML::Tagset, Test::NoWarnings and Test::Warn. This is
a repository snapshot, not a guarantee about future repository contents.

The upstream default action runs all 14 `t/*.t` files with 173 planned
assertions. They remain unchanged, including upstream TODO cases. Two
`t/developer/*.t` POD tests are outside that default action and are not
claimed as executed. A local macOS Perl 5.34 scratch `make test` failed:
13 files could not start because `Test::NoWarnings` is absent locally; only
`t/base.t` ran (35 assertions). The target SPEC requires the official
`perl(Test::NoWarnings)` provider, but only exact-head target CI can establish
the complete suite. A local source staging install produced three modules and
three manual pages. The installed-RPM smoke checks an actual paragraph
conversion through the packaged module; it is not a public publication test.
