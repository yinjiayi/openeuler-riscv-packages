<!-- SPDX-License-Identifier: Apache-2.0 -->
# libstatistics-welford-perl

The frozen inventory identifies Debian's `libstatistics-welford-perl` 0.02;
Debian trixie carries source version 0.02-3. The official
[Statistics-Welford 0.02](https://metacpan.org/dist/Statistics-Welford)
CPAN tarball is 2,166 bytes with SHA-256
`f70cd4a3240b3d32fcee821dad3dbcb4d06017f56f17227f9970815709477043`,
matching KAARE's publisher `CHECKSUMS`. The single-root archive contains
only regular source, metadata and test files; no links, special files,
vendored code or third-party data. The `source_repository` metadata points
to this distribution's MetaCPAN source page; upstream metadata does not
advertise a public VCS repository. Its sole module's `COPYRIGHT` POD grants
redistribution under the same terms as Perl 5, consistent with `Build.PL`
and `META.yml`. RPM metadata selects the GPL-1.0-or-later alternative and
does not infer a version for the separate Artistic option. The POD is
retained in the installed manpage and SRPM.

The checksum-bound official openEuler 24.03 LTS SP3 RVA23 primary metadata
(SHA-256 `fdb1663ee6c803e8efcc83c19b7a1548f047f08abba8a52f5fe623b222064d1a`)
has no `perl-Statistics-Welford` RPM or `perl(Statistics::Welford)` provider.
The module uses only core Perl. The target provides `perl(Module::Build) =
0.4234`, `perl(Test::Pod) = 1.52` and `perl(Test::Pod::Coverage) = 1.10`;
these are explicit build dependencies so the default POD tests do not skip.
This is a snapshot check, not a guarantee about later repository state.

All three original default test files remain unchanged. Local source-only
`perl Build.PL --installdirs vendor && ./Build && ./Build test` passed the
18 functional assertions and one POD syntax assertion. The POD coverage
file self-skipped locally because this macOS host lacks its optional test
module; target BuildRequires must cause that check to execute. These are
not RPM or RISC-V build results. Target CI must run the full original suite,
install the resulting RPM and check count, extrema, mean, variance and
standard deviation through the installed module. Those are functional
checks under QEMU user mode, not a native RISC-V performance claim. A
successful PR build is not evidence of public repository publication.
