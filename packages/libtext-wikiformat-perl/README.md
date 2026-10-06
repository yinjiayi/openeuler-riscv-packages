<!-- SPDX-License-Identifier: Apache-2.0 -->
# libtext-wikiformat-perl

The frozen inventory's exact `libtext-wikiformat-perl` key maps to Ubuntu and
Debian source version 0.81-1. This package uses the official stable
[Text-WikiFormat 0.81](https://metacpan.org/dist/Text-WikiFormat) CPAN release.
The HTTPS tarball SHA-256
`e43cd995ad9157a7e839d993ee7b6c4d1854947e557d096d9d5aaf74507fab33`
matches the publisher's `CHECKSUMS` entry. Its single-root archive has no
traversal paths, symlinks or special files. The included `ARTISTIC` and `GPL`
texts, README, `Build.PL` and both module POD notices establish Perl dual
terms, resolving the frozen automated `license-blocked` marker for this
specific release.

The official openEuler 24.03 LTS SP3 RVA23 `everything` primary metadata
(SHA-256 `fdb1663ee6c803e8efcc83c19b7a1548f047f08abba8a52f5fe623b222064d1a`)
contains neither `perl-Text-WikiFormat` nor a `perl(Text::WikiFormat)`
provider, while it provides `perl(Module::Build)`, `perl(URI::Escape)` and
`perl(Scalar::Util)`. This is a snapshot check, not a guarantee about future
repository contents.

All 14 default upstream `t/*.t` files ran locally using unmodified source.
Of 143 TAP checks, 142 passed and one, in `t/embedded-links.t`, failed under
upstream's explicit TODO marker for unsupported MediaWiki link-handler
behavior. The harness reports success, but that TODO case is not a passing
feature test. Two `t/developer/*.t` POD tests are intentionally outside
upstream's default `./Build test` and are not counted as passed. No tests or
features have been disabled here.

A source-level staging install yielded both modules and both manual pages,
all listed in the SPEC. The installed-RPM smoke exercises a supported plain
paragraph formatting path. Target RPM build, the complete default suite and
installed smoke remain for CI to verify; successful PR artifacts alone do not
prove public repository publication.
