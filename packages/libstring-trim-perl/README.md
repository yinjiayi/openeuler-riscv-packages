<!-- SPDX-License-Identifier: Apache-2.0 -->
# libstring-trim-perl

The frozen inventory's exact `libstring-trim-perl` key maps to Ubuntu source
version 0.005-4. This package uses the official stable
[String-Trim 0.005](https://metacpan.org/dist/String-Trim) CPAN release; it is
distinct from Text::Trim. Its HTTPS tarball SHA-256
`b169e20b02476f308fec0425c75077fd6a851f578b4ea3703e6220659d73b31f`
matches the publisher's `CHECKSUMS` entry. The single-root archive contains
only regular files and directories, with no traversal, links or special
files. The included LICENSE and module POD expressly grant the same terms as
Perl itself despite frozen metadata reporting an unknown license.

The official openEuler 24.03 LTS SP3 RVA23 `everything` primary metadata
(SHA-256 `fdb1663ee6c803e8efcc83c19b7a1548f047f08abba8a52f5fe623b222064d1a`)
contains neither `perl-String-Trim` nor a `perl(String::Trim)` provider. This
is a snapshot check, not a guarantee about future repository contents.
Upstream's runtime requirement is Perl core Exporter 5.57 or newer.

The unmodified upstream local `make test` ran all nine default `t/*.t` files:
20 assertions passed across string, undef, array, arrayref, hash and hashref
cases. The `xt/author` and `xt/release` files are nondefault and are not
claimed as passed functional tests. A source-level staging install yielded
the module and manual page, both listed in the SPEC. Installed-RPM smoke
tests the version, generated Provides, string trim and array trim. Target
RPM build, complete default suite and installed smoke remain for CI to
verify; successful PR artifacts alone do not prove public repository
publication.
