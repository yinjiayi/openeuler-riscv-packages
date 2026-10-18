<!-- SPDX-License-Identifier: Apache-2.0 -->
# libstring-koremutake-perl

The frozen inventory's exact `libstring-koremutake-perl` key maps to Ubuntu
and official CPAN source version 0.30. Its HTTPS tarball SHA-256
`2d61f02e8fca2e9b3097678b1472f84b825b2cca95c1eb1a99d1593024d537ba`
matches the publisher's `CHECKSUMS`. The inspected archive has one root and
only regular files and directories, with no traversal, links or special
files. The included README and module POD explicitly permit redistribution
and modification under the same terms as Perl itself. This resolves the
frozen inventory's historical `license-blocked` finding for this release;
the RPM maps that grant to GPL-1.0-or-later OR Artistic-1.0-Perl and installs
the README as `%license`.

The official openEuler 24.03 LTS SP3 RVA23 `everything` primary metadata
(SHA-256 `fdb1663ee6c803e8efcc83c19b7a1548f047f08abba8a52f5fe623b222064d1a`)
has neither `perl-String-Koremutake` nor a `perl(String::Koremutake)`
provider. It contains Error 0.17029 (Epoch 1), Test::Exception 0.43 and
Test::Pod::Coverage 1.10. This snapshot check is not a guarantee about
future repository contents.

The unchanged upstream default `make test` selects three files. Locally,
`t/simple.t` passed its 34 checks and `t/pod.t` passed one check;
`t/pod_coverage.t` reported SKIP because Test::Pod::Coverage is not installed
on the local Mac. The SPEC requires that module so target CI must actually
run POD coverage. One upstream `dies_ok` assertion mistakenly calls
`koremutake_to_intger` (missing an `e`), so its success does not test malformed
input handling by the real `koremutake_to_integer` method. The installed-RPM
smoke therefore asserts five encode/decode round trips and a nonzero failure
for malformed input through the correctly spelled method. Those checks
passed against the unmodified source locally, but target RPM build, full
default suite and installed smoke remain for CI to verify. Successful PR
artifacts alone do not prove public repository publication.
