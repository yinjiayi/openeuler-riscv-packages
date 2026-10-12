<!-- SPDX-License-Identifier: Apache-2.0 -->
# libtext-sprintfn-perl

The frozen inventory's exact `libtext-sprintfn-perl` key maps to Ubuntu and
Debian source 0.090-2 and the official [Text-sprintfn
0.090](https://metacpan.org/dist/Text-sprintfn) CPAN release. Debian's
original tarball MD5 `8a9c7a956a1a738eae2b0f0af7ff9a69` matches the
official CPAN archive byte for byte. The publisher's `CHECKSUMS` entry and
downloaded HTTPS archive both have SHA-256
`1ff9cfbb6a2d3b667109a4751b8421bd81802166c7be2fc367df57dd7a39fcdc`.
The 19-entry archive has one root without traversal, links or special files.
Included LICENSE and module POD grant Perl dual GPL/Artistic terms, resolving
the frozen automated `license-blocked` decision for this release.

The official openEuler 24.03 LTS SP3 RVA23 `everything` primary metadata,
`primary.xml.zst` SHA-256
`fdb1663ee6c803e8efcc83c19b7a1548f047f08abba8a52f5fe623b222064d1a`,
contains neither `perl-Text-sprintfn` nor a `perl(Text::sprintfn)` provider;
the module has no external runtime dependencies. This is a snapshot check,
not a guarantee about future repository contents.

`%check` retains the full default upstream invocation. `00-compile.t` and
`01-basics.t` passed 30 assertions with local Perl 5.34.1. The three
`author-*` files report upstream-defined SKIP unless `AUTHOR_TESTING` is set;
they are not counted as passing. Two historical cases inside `01-basics.t`
are already commented out by upstream for Perl version/warning compatibility,
and neither is claimed as validated. No test is removed or patched here. A
source-level staging install yielded the module and man page, both listed in
the SPEC; installed-RPM smoke checks named formatting. Target CI must prove
RPM build, the same default test result, and installation.

Successful PR CI artifacts alone do not prove public RPM repository publication.
