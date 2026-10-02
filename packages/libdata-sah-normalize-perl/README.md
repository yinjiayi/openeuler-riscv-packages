<!-- SPDX-License-Identifier: Apache-2.0 -->
# Data::Sah::Normalize 0.051

The frozen Ubuntu `libdata-sah-normalize-perl` 0.051-2 inventory key maps to
official stable [Data-Sah-Normalize 0.051](https://metacpan.org/dist/Data-Sah-Normalize).
Publisher CHECKSUMS and the independently downloaded 17,631-byte HTTPS
archive agree on SHA-256
`5e1d880bac8b887980d3311487bce6b67a15a78e74eb46d7a4c7d265c84e7758`.
The archive has one top-level tree and only regular files and directories.

Bundled `LICENSE`, release README and the sole installed PM POD explicitly
grant redistribution under Perl 5 terms from copyright holder perlancar.
The LICENSE spells out GPL version 1 or later or Artistic 1.0. No source,
test, or fixture file has a conflicting third-party notice.

The official openEuler 24.03 LTS SP3 riscv64/RVA23 primary contains no
`perl-Data-Sah-Normalize` or `perl(Data::Sah::Normalize)` provider. It
uniquely supplies ExtUtils::MakeMaker, Exporter, Test::Exception, Test::More,
and the core compile-test modules File::Spec, IO::Handle, and IPC::Open3.

Unmodified upstream `make test` selects all five default files. The two
functional files pass six assertions locally; three author-only POD/critic
files self-skip unless `AUTHOR_TESTING` is set by upstream design. This
package does not claim those optional author tests passed. Exact-head target
CI must reproduce the functional coverage and explicit skips, build physical
RPM/SRPM products, install with DNF, and pass the installed shortcut/schema
normalization and invalid-input smoke. PR CI is not RPM publication.
