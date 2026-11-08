<!-- SPDX-License-Identifier: Apache-2.0 -->
# libtext-rewriterules-perl

The frozen inventory's `libtext-rewriterules-perl` key maps to Ubuntu
`0.25-2` and Debian `0.25-1.1`. This package uses the official stable
[Text::RewriteRules 0.25](https://metacpan.org/dist/Text-RewriteRules) CPAN
release. Its HTTPS tarball SHA-256
`ab7ea0dbb7deee56a7f927bbb8ca15b18f76088f45c5543d12d8ba2cf4d3dd6f`
matches the publisher's `CHECKSUMS` entry. The single-root archive contains
only regular files and directories, with no traversal or special files.

The included README and module POD both grant redistribution under the same
terms as Perl itself, which this repository maps to `GPL-1.0-or-later OR
Artistic-1.0-Perl`. This resolves the frozen automated `license-blocked`
decision for this release. The README carries the upstream notice and is
installed as `%license`; the archive has no separate license-text file.

The official openEuler 24.03 LTS SP3 RVA23 `everything` primary metadata
(SHA-256 `fdb1663ee6c803e8efcc83c19b7a1548f047f08abba8a52f5fe623b222064d1a`)
contains neither `perl-Text-RewriteRules` nor a `perl(Text::RewriteRules)`
provider. It does provide `perl(Filter::Simple)` 0.94, satisfying upstream's
minimum 0.78, and `perl(Test::More)`. This is a snapshot check, not a
guarantee about future repository contents.

All 13 functional default upstream `t/*.t` files passed 207 assertions
locally with source unmodified. The other two default files are author-only
POD checks and skip under upstream's normal non-author conditions; they are
not removed or suppressed by the SPEC. A source-level staging install yielded
the module, `textrr` command, and their manual pages, all listed in `%files`.
Installed-RPM smoke checks both in-process rewriting and the compiled-command
path. Target RPM build, default tests, installed smoke, and any public
publication remain for CI or later evidence to verify.
