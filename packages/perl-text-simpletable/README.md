<!-- SPDX-License-Identifier: Apache-2.0 -->
# perl-text-simpletable

The frozen inventory's `perl-text-simpletable` row records AUR 2.07-1 and
was marked stale because its AUR metadata had aged past the discovery
threshold. Ubuntu independently ships the same 2.07 upstream version, and
the official stable [Text-SimpleTable 2.07](https://metacpan.org/dist/Text-SimpleTable)
CPAN release remains available. Its 10,125-byte HTTPS tarball SHA-256 is
`256d3f38764e96333158b14ab18257b92f3155c60d658cafb80389f72f4619ed`,
matching MRAMBERG's publisher `CHECKSUMS`; the Ubuntu original tarball MD5
also matches. The archive contains only one rooted tree of regular files
and directories, with no links, special files or vendored code. Its included
`LICENSE` grants Artistic-2.0 for the package; module POD, Makefile.PL and
metadata agree. The license file is installed with the RPM.

The official openEuler 24.03 LTS SP3 RVA23 primary metadata (SHA-256
`fdb1663ee6c803e8efcc83c19b7a1548f047f08abba8a52f5fe623b222064d1a`)
has no `perl-Text-SimpleTable` or `perl(Text::SimpleTable)` provider. It does
provide Test::Pod 1.52, Test::Pod::Coverage 1.10, Unicode::GCString 2013.10
from perl-Unicode-LineBreak, and MIME::Charset 1.013.1. The last dependency
is explicit because the target Unicode::GCString supplier does not declare
its lazy MIME::Charset import. These are snapshot checks, not guarantees
about later repository state.

All five original upstream `t/*.t` files remain unchanged. A local macOS
default source run passed ten assertions; CJK skipped because its module
was unavailable, POD skipped without `TEST_POD`, and POD coverage skipped
because its local module was unavailable.
The target SPEC explicitly installs those dependencies and sets `TEST_POD=1`
to exercise the ASCII, CJK, POD and POD-coverage cases. Only exact-head
target CI can establish whether they all pass. Installed-RPM smoke checks
the RPM provider and ASCII and Unicode rendering. A successful PR build
does not by itself prove publication to the public repository.
