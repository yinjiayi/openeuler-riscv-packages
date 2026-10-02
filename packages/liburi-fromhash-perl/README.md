<!-- SPDX-License-Identifier: Apache-2.0 -->
# liburi-fromhash-perl

The frozen Ubuntu `liburi-fromhash-perl` 0.05-2 row in
`discovery-20260808T165000Z-9a89920c269462cd` maps to the official CPAN
URI-FromHash 0.05 release. Its 19,907-byte archive SHA-256
`a7cac5bccee9f2e2d8ad0f605400163712cd0ac64df2fb834f760fb49f2f6fd0`
matches the publisher's `CHECKSUMS`. The archive has one root with regular
text files and directories, and no traversal path or symlink.

The bundled LICENSE, README and module POD explicitly grant Artistic
License 2.0 for the distribution. The test and build files carry no
conflicting notice or binary fixture. The RPM uses `Artistic-2.0`.

Checksum-verified official openEuler 24.03 LTS SP3 `riscv64` RVA23 primary
metadata (SHA-256
`fdb1663ee6c803e8efcc83c19b7a1548f047f08abba8a52f5fe623b222064d1a`)
has no same-name RPM or `perl(URI::FromHash)` provider. It uniquely supplies
Params::Validate, URI, Exporter, Carp, Test::Fatal, Test::More and MakeMaker.

All 16 original `t/*.t` files remain unchanged. A fresh local default source
test passed 23 assertions across `t/uri.t` and `t/00-report-prereqs.t`. The
six `author-*.t` and eight `release-*.t` files each explicitly skip unless
upstream `AUTHOR_TESTING` or `RELEASE_TESTING`, respectively, is enabled.
These 14 skips are not target functional-test passes; the package neither
removes the files nor changes their gates.

Installed-RPM smoke checks URI construction, parsing and round-trip behavior,
plus the URI object return path, using the installed module. Exact-head
hosted target CI and physical RPM/SRPM audit remain acceptance evidence;
PR-only success does not imply public repository publication.
