<!-- SPDX-License-Identifier: Apache-2.0 -->
# libstatistics-contingency-perl

The frozen inventory identifies Debian's `libstatistics-contingency-perl`
0.09; Debian trixie carries source version 0.09-2. The official KWILLIAMS
CPAN `Statistics-Contingency-0.09.tar.gz` is 15,211 bytes with SHA-256
`4b50621c4974937564ce76b523e9073db50e67de6f5bfae92f088b3ae22975bf`,
matching the publisher's `CHECKSUMS`. The single-root archive contains only
regular source, metadata, license and test files; there are no links,
special files, vendored code or third-party datasets. Its distribution-wide
`LICENSE` and module POD grant the same terms as Perl 5: GPL version 1 or
later, or the Artistic License. RPM metadata selects the explicit
GPL-1.0-or-later alternative. Debian's `Files: *` copyright record agrees.

The checksum-bound official openEuler 24.03 LTS SP3 RVA23 primary metadata
(SHA-256 `fdb1663ee6c803e8efcc83c19b7a1548f047f08abba8a52f5fe623b222064d1a`)
has no `perl-Statistics-Contingency` RPM or
`perl(Statistics::Contingency)` provider. It does provide the hard runtime
`perl(Params::Validate) = 1.31`, plus Module::Build and Test for the original
suite. Explicit runtime and build dependencies cover that closure. This
is a snapshot, not a guarantee about later repository state.

Both original default test files are retained unchanged. Local source-only
`perl Build.PL --installdirs vendor && ./Build && ./Build test` passed the
24 functional assertions in `t/01-basic.t`; `t/author-critic.t` self-skipped
because upstream gates it on `AUTHOR_TESTING`. This upstream author-only
skip is not relabeled as executed coverage. The target `%check` retains
the complete default suite, and installed smoke checks constructor,
precision, recall and accuracy after DNF installation. These QEMU-user
functional checks cannot establish native RISC-V behavior or public RPM
repository publication.
