<!-- SPDX-License-Identifier: Apache-2.0 -->
# libmodule-optional-perl

The frozen inventory key `libmodule-optional-perl` records Module::Optional
0.03. This package uses the official [CPAN release](https://metacpan.org/dist/Module-Optional).
Its HTTPS archive SHA-256
`971170aa63cbfa7f55a8d6f6e4d3d4e77449aa3a5a3ee6650518d36bbca134a8`
matches publisher `CHECKSUMS`; the archive contains only regular files and
directories, no links, special files or traversal paths.

The distribution `LICENSE` expressly grants the same terms as Perl itself:
GPL version 1 or later, or Artistic License 1.0. The main module and README
repeat this grant. The companion `Params::Validate::Dummy` module and example
carry no conflicting notice; they are included in the same licensed archive.
The RPM metadata uses `GPL-1.0-or-later OR Artistic-1.0-Perl`.

The checksum-bound official openEuler 24.03 LTS SP3 RVA23 `everything`
primary metadata (SHA-256
`fdb1663ee6c803e8efcc83c19b7a1548f047f08abba8a52f5fe623b222064d1a`)
has neither this RPM nor a `perl(Module::Optional)` provider. It supplies
the upstream-declared Test::Simple 1.302198, and Test::Pod 1.52 plus
Test::Pod::Coverage 1.10 for both upstream POD test files. This is a snapshot
check, not a guarantee about future repository contents.

All six default test files are unchanged. A clean local Perl 5.34 source run
passed 19 assertions; `t/pod_coverage.t` followed its upstream skip because
Test::Pod::Coverage is absent locally. The SPEC explicitly requires that
provider at target build time, so target CI must settle the full suite without
that local skip. A scratch staging install included both Perl modules and
both man pages. The installed-RPM smoke checks their generated Provides,
module version and the dummy validator behavior. PR artifacts are not public
RPM/SRPM publication; target build and installed smoke remain CI evidence.
