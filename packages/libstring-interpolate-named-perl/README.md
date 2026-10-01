<!-- SPDX-License-Identifier: Apache-2.0 -->
# libstring-interpolate-named-perl

The frozen inventory's exact `libstring-interpolate-named-perl` key maps to
Ubuntu and official CPAN source version 1.06. The official HTTPS tarball
SHA-256
`012cca57baf8335b163c734b789d5966dde47f0bd8a579433f4852ca666fffe2`
matches the publisher's `CHECKSUMS`. The inspected archive has one root and
only regular files and directories, with no traversal, links or special
files. Its README and module POD expressly grant redistribution and
modification under the same terms as Perl itself, represented as
GPL-1.0-or-later OR Artistic-1.0-Perl. The README is installed as `%license`.

The official openEuler 24.03 LTS SP3 RVA23 `everything` primary metadata
(SHA-256 `fdb1663ee6c803e8efcc83c19b7a1548f047f08abba8a52f5fe623b222064d1a`)
has neither `perl-String-Interpolate-Named` nor a
`perl(String::Interpolate::Named)` provider. No non-core runtime module is
required. This snapshot check is not a guarantee about future contents.

All eight unmodified default upstream `t/*.t` files ran locally: 449 tests
passed without skips. Their `.dat` fixtures stay in the verified source
archive and are available to `%check`. A source-level staged install yielded
the module and manual page listed in the SPEC. Installed-RPM smoke confirms
the module version and named interpolation from the upstream example. Target
RPM build, complete default suite and installed smoke remain for CI to
verify; successful PR artifacts alone do not prove public publication.
