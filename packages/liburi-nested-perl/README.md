<!-- SPDX-License-Identifier: Apache-2.0 -->
# liburi-nested-perl

The frozen Ubuntu `liburi-nested-perl` 0.10-4 row in
`discovery-20260808T165000Z-9a89920c269462cd` maps to the official CPAN
URI-Nested 0.10 release. Its 6,170-byte archive SHA-256
`e1971339a65fbac63ab87142d4b59d3d259d51417753c77cb58ea31a8233efaf`
matches the publisher's `CHECKSUMS`. The archive has a single root and only
regular text files and directories, with no symlinks or traversal paths.

The README and module POD grant redistribution under the same terms as Perl
5; Build.PL and release metadata agree, and tests have no conflicting
notice. The RPM records the Perl 5 dual SPDX expression
`GPL-1.0-or-later OR Artistic-1.0-Perl`. The upstream archive does not ship
a separate LICENSE file, so the grant-bearing README is installed as the
license document.

Checksum-verified official openEuler 24.03 LTS SP3 `riscv64` RVA23 primary
metadata (SHA-256
`fdb1663ee6c803e8efcc83c19b7a1548f047f08abba8a52f5fe623b222064d1a`)
has no same-name RPM or `perl(URI::Nested)` provider. It uniquely supplies
URI, URI::QueryParam, Carp, Module::Build and Test::More.

The upstream source uses `URI->new` and `Carp::croak` without importing URI
or Carp. Its original tests import URI first, hiding the direct-use failure:
`perl -Ilib -MURI::Nested -e 'URI::Nested->new("http://example.com")'`
fails before the patch. A two-line package-local patch loads those existing
runtime dependencies. It applies cleanly to the pinned source, does not
change the public API, and keeps both original `t/*.t` files untouched.
Both upstream files passed all 87 assertions before and after the patch;
an additional direct-import regression passes only after it. Installed-RPM
smoke repeats that regression and checks nested URI parsing.

Exact-head hosted target CI and physical RPM/SRPM audit remain acceptance
evidence; a successful PR build does not imply public repository publication.
