<!-- SPDX-License-Identifier: Apache-2.0 -->
# liburi-normalize-perl

The frozen Ubuntu `liburi-normalize-perl` 0.002-2 source maps to the official
CPAN URI-Normalize 0.002 release. Its full archive SHA-256
`e08b96b53f45bc2e4b1ffb1eddbbf85ae89e6177c7ad79ea112a2b92040b1e83`
matches the publisher's `CHECKSUMS`. The archive has one root, regular
text files and directories only, and no traversal path or symlink.

The README, `URI::Normalize` module POD, and bundled LICENSE grant the same
terms as Perl 5. Build files and tests have no contradictory notice. The
RPM records the GPL-1.0-or-later or Artistic-1.0-Perl choice.

Checksum-verified official openEuler 24.03 LTS SP3 `riscv64` RVA23 primary
metadata (SHA-256
`fdb1663ee6c803e8efcc83c19b7a1548f047f08abba8a52f5fe623b222064d1a`)
has no same-name RPM or `perl(URI::Normalize)` provider. It uniquely
supplies the needed URI, Exporter, Scalar::Util, MakeMaker and Test::More
providers. This is an official-repository snapshot check.

All three original `t/*.t` files remain unchanged. A fresh local default
source test passed all 12 functional assertions. The two author-only POD
tests intentionally skip unless `AUTHOR_TESTING` is set; their
`Pod::Coverage::TrustPod` dependency is absent from the target and they are
not part of the upstream default test path. No default test or feature is
disabled by this package.

The installed-RPM smoke verifies the module version, URI normalization and
dot-segment removal using the installed package. Exact-head hosted target
CI and physical RPM/SRPM audit remain the acceptance evidence. PR-only
success does not imply public repository publication.
