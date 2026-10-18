<!-- SPDX-License-Identifier: Apache-2.0 -->
# libstring-expand-perl

The frozen inventory's exact `libstring-expand-perl` key maps to Ubuntu and
Debian source version 0.04-5. This package uses the official stable
[String-Expand 0.04](https://metacpan.org/dist/String-Expand) CPAN release.
The HTTPS tarball SHA-256
`96a18d78fbe0bcb3c5e41d23ca000d30c830f759f7fb745892b9a8eded6c4b44`
matches the publisher's `CHECKSUMS` entry. Its single-root archive has no
traversal paths, symlinks or special files. The included LICENSE grants the
same terms as Perl itself, explicitly GPL-1-or-later or Artistic License;
the module header confirms these terms. This resolves the frozen automated
`license-blocked` marker for this specific release, rather than treating
the historical marker as a waiver.

The official openEuler 24.03 LTS SP3 RVA23 `everything` primary metadata
(SHA-256 `fdb1663ee6c803e8efcc83c19b7a1548f047f08abba8a52f5fe623b222064d1a`)
contains neither `perl-String-Expand` nor a `perl(String::Expand)` provider,
and does provide `perl(Test::Exception)` and `perl(Test::Pod)` version 1.52.
This is a snapshot check, not a guarantee about future repository contents.

All four unmodified default upstream `t/*.t` files ran locally: 16 assertions
passed, including the POD suite. Test::Pod is a required build dependency so
that the optional upstream POD suite does not silently skip on the target.
No tests were disabled. A source-level staging install yielded one module and
one manual page, both listed in the SPEC. Installed-RPM smoke checks version,
generated Provides, simple and chained expansion, and error behavior. Target
RPM build, the complete default suite and installed smoke remain for CI to
verify; successful PR artifacts alone do not prove public repository
publication.
