<!-- SPDX-License-Identifier: Apache-2.0 -->
# libtest-bits-perl

The frozen inventory's exact `libtest-bits-perl` key maps to official stable
CPAN Test::Bits 0.02. The 9,651-byte release tarball SHA-256
`a9826f56483a27e2c63156590f328a3633e30375c10dfc89f6690e3929de0bc3`
matches publisher `CHECKSUMS`. The archive has one root and only regular
files and directories, without traversal, links or special files.

The archive includes the full Artistic License 2.0 in `LICENSE`, and module
POD agrees. The official openEuler 24.03 LTS SP3 RVA23 `everything` primary
metadata (SHA-256 `fdb1663ee6c803e8efcc83c19b7a1548f047f08abba8a52f5fe623b222064d1a`)
contains neither `perl-Test-Bits` nor a `perl(Test::Bits)` provider. It does
provide List::AllUtils, Test::Fatal, Test::More and Test::Tester. The snapshot
does not guarantee future repository contents.

Unmodified upstream `make test` was attempted locally, but macOS Perl 5.34
lacks List::AllUtils, so the compile and functional tests failed before
assertions could run; this is not evidence of a target failure or success.
The target SPEC includes that dependency and preserves the complete original
`%check`. Upstream author/release tests are environment-gated in the release
archive and remain unchanged. Installed-RPM smoke checks the package/module
provider, version and a byte comparison. Target RPM build, default tests and
installed smoke remain for CI to verify; PR artifacts alone do not prove
public repository publication.
