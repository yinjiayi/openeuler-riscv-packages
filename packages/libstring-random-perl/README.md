<!-- SPDX-License-Identifier: Apache-2.0 -->
# libstring-random-perl

The frozen inventory's exact `libstring-random-perl` key maps to official
stable CPAN String::Random 0.32. Its HTTPS release tarball SHA-256
`9d93c679a34ffa26d3b4fa0837caed1cd2e67d76572818b91e97dea734705246`
matches the publisher's `CHECKSUMS`. All 39 archive entries lie under one
root and are regular files or directories, with no traversal or links.

The archived `LICENSE` states the same terms as Perl itself: GPL-1.0-or-later
or Artistic-1.0-Perl. README and module POD repeat those terms. The official
openEuler 24.03 LTS SP3 RVA23 `everything` primary metadata (compressed
SHA-256 `fdb1663ee6c803e8efcc83c19b7a1548f047f08abba8a52f5fe623b222064d1a`,
open SHA-256 `57be74ba1e5023e98fc645095923f23a3260c3a11c3f4785d89eac353749e84a`)
has neither `perl-String-Random` nor `perl(String::Random)`. Its
`perl(Module::Build)` provider is present. A future repository generation
must be checked again before merger.

Unmodified upstream `./Build test` ran all nine default `t/` files and
202 assertions locally without skips. Four separate `xt/author` and two
`xt/release` files are author/release checks, outside the default test target;
they are not claimed as passing. A source-level staged install yielded the
module and man page listed in the SPEC. The installed-RPM smoke checks the
generated Perl Provide, version and deterministic pattern/regex output.
Target RPM build, default tests and installed smoke remain for exact-head
CI to verify; PR artifacts alone do not prove public repository publication.

String::Random uses Perl's `rand`, not a cryptographically secure random
source. Do not use its output for passwords, tokens or other secrets.
