<!-- SPDX-License-Identifier: Apache-2.0 -->
# liburi-todisk-perl

The frozen inventory's exact `liburi-todisk-perl` key maps to Ubuntu source
1.12-3 and upstream URI-ToDisk 1.12. The official stable
[CPAN release](https://metacpan.org/dist/URI-ToDisk) SHA-256
`b2d9a645a54c5c153fc032a4db19d0c6c8fc4eac41b6b7614ef6c8184a6dfc95`
matches publisher `CHECKSUMS`. The single-root archive has no traversal
paths, symlinks or special files. The included LICENSE explicitly grants
GPL-1-or-later or Artistic terms; README and module POD repeat the Perl grant,
and no shipped file has a contradictory notice. The eight bundled
`inc/Module/Install*.pm` files were compared to the corresponding modules in
official CPAN Module-Install 0.68 (SHA-256
`f6aa0c315cbc9456f642db3de8d2315d658f0a59d46aa0946737fee09d2e293c`).
They have no added substantive lines beyond generated `#line` markers; POD
and comments were stripped. That upstream release's own LICENSE grants the
same Perl terms. These files are only source-build helpers, not installed in
the binary RPM.

Official openEuler 24.03 LTS SP3 RVA23 `everything` primary metadata (SHA-256
`fdb1663ee6c803e8efcc83c19b7a1548f047f08abba8a52f5fe623b222064d1a`)
contains neither `perl-URI-ToDisk` nor a `perl(URI::ToDisk)` provider. It
supplies Clone 0.46, Params::Util 1.07, URI 5.10, List::Util 1.63,
File::Spec 3.88 and Test::More 1.302198. This is a snapshot check, not a
guarantee about future repository contents.

All four unchanged default upstream `t/*.t` files ran locally. The two
functional suites passed 130 assertions; the other two are upstream
author-only files that skip by default unless `AUTOMATED_TESTING` is set.
No test was removed or disabled. The functional test manipulates path
strings but performs no filesystem writes. Installed-RPM smoke likewise
checks URI/path mapping without creating a file. Target RPM build, test and
installed smoke remain for exact-head CI; successful PR artifacts do not
establish public repository publication.
