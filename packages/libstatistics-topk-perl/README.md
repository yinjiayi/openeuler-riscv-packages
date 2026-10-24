<!-- SPDX-License-Identifier: Apache-2.0 -->
# libstatistics-topk-perl

The frozen inventory identifies Debian's `libstatistics-topk-perl` 0.02;
Debian trixie carries source version 0.02-2. The official GRAY CPAN
`Statistics-TopK-0.02.tar.gz` is 5,364 bytes with SHA-256
`9b83f0012f18034c906f8d10bcfcd72976529375fd9edc9b5d1c2b9d7e6f8955`,
matching the publisher's `CHECKSUMS`. The single-root archive has only
regular source, metadata and test files, with no links, special files,
vendored code or third-party datasets. The module POD grants redistribution
under the same terms as Perl, consistent with `Makefile.PL` and `META.json`.
Debian's `Files: *` record identifies the GPL-1-or-later or Artistic grant;
RPM metadata selects the explicit GPL-1.0-or-later alternative. The grant
is retained in the SRPM and installed module documentation.

The checksum-bound official openEuler 24.03 LTS SP3 RVA23 primary metadata
(SHA-256 `fdb1663ee6c803e8efcc83c19b7a1548f047f08abba8a52f5fe623b222064d1a`)
has no `perl-Statistics-TopK` RPM or `perl(Statistics::TopK)` provider.
The module uses core Perl only; the target provides `perl(Test::More) =
1.302198`, satisfying upstream's 0.98 default-test minimum. This is a
snapshot check, not a guarantee about later repository state.

All three original default test files remain unchanged. Local source-only
`perl Makefile.PL INSTALLDIRS=vendor && make test` passed all 8 assertions
without skips. Six files in `xt/` are upstream author/release-only tests,
not part of the default `t/*.t` suite; they are preserved in the source
archive, not represented as executed default coverage. Target `%check`
must run every default file. Installed smoke checks exact counts within the
three-slot capacity and rejection of an invalid constructor argument.
These QEMU-user functional checks do not prove probabilistic accuracy,
native RISC-V performance or public repository publication.
