<!-- SPDX-License-Identifier: Apache-2.0 -->
# libstatistics-lite-perl

The frozen inventory identifies Debian's `libstatistics-lite-perl` 3.62;
Debian trixie carries source version 3.62-1.1. The official
[Statistics-Lite 3.62](https://metacpan.org/dist/Statistics-Lite) CPAN tarball
is 5,811 bytes with SHA-256
`1076c514aa860f7638c665ad611b3a8c33344b66ad690e5b290b9c8476ad9aa7`,
matching BRIANL's publisher `CHECKSUMS`. The single-root archive contains
only regular source, metadata and test files; no links, special files,
vendored code or third-party data. The module's `COPYRIGHT AND LICENSE`
section grants the library the same terms as Perl 5, consistent with
`Makefile.PL` and `META.json`. RPM metadata selects the GPL-1.0-or-later
alternative and does not infer a version for the separate Artistic option.
The module POD is retained in the installed manpage and SRPM.

The checksum-bound official openEuler 24.03 LTS SP3 RVA23 primary metadata
(SHA-256 `fdb1663ee6c803e8efcc83c19b7a1548f047f08abba8a52f5fe623b222064d1a`)
has no `perl-Statistics-Lite` RPM or `perl(Statistics::Lite)` provider.
The distribution uses only Perl's core `Exporter`; the original build and
test suite use target-provided MakeMaker and Test::More. This is a snapshot
check, not a guarantee about later repository state.

All nine original default test files remain unchanged. The upstream
`Makefile.PL` stages the top-level `Lite.pm` as `Statistics/Lite.pm`; direct
`prove -I.` cannot load it, while the intended local `perl Makefile.PL &&
make test` passed all 68 assertions with no skips. That local source-only
run is not an RPM or RISC-V build. Target CI must run the unchanged suite,
install the resulting RPM and check mean, median, mode, variance and
frequencies through the installed module. Those checks establish functional
behavior under QEMU user mode, not native RISC-V performance. A successful
PR build is not evidence of public repository publication.
