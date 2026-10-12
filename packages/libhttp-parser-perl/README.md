<!-- SPDX-License-Identifier: Apache-2.0 -->
# libhttp-parser-perl

The frozen inventory's exact `libhttp-parser-perl` key maps to Ubuntu source
0.06-4 and upstream HTTP-Parser 0.06. This package uses the official stable
[HTTP-Parser 0.06](https://metacpan.org/dist/HTTP-Parser) CPAN release.
The HTTPS tarball SHA-256
`f8c5a1e1cbd8f2775bd3d1ce5facc8431f059108bf575a0c8dbda432e5c0bc45`
matches the publisher's `CHECKSUMS` entry. Its single-root archive contains
only regular files, with no traversal paths or links. README grants
redistribution under the same terms as Perl itself; Makefile.PL and META.yml
both identify the same `perl` license. No shipped file has a contradictory
notice. The RPM records the conventional Perl 5 dual-license SPDX expression.

The official openEuler 24.03 LTS SP3 RVA23 `everything` primary metadata
(SHA-256 `fdb1663ee6c803e8efcc83c19b7a1548f047f08abba8a52f5fe623b222064d1a`)
contains neither `perl-HTTP-Parser` nor a `perl(HTTP::Parser)` provider. It
supplies HTTP::Request, HTTP::Response, URI, ExtUtils::MakeMaker and
Test::More. This is a snapshot check, not a claim about future repositories.

The sole unchanged default upstream `t/1.t` file ran in an isolated source
tree: 22 assertions passed with no skips. It checks request and response
parsing, headers and URI behavior without network access. Installed-RPM
smoke independently checks both request and response parsing. Target RPM
build, tests and installed smoke remain for exact-head CI to verify; PR
artifacts alone do not establish public repository publication.
