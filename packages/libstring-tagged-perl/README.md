<!-- SPDX-License-Identifier: Apache-2.0 -->
# libstring-tagged-perl

The frozen inventory's exact `libstring-tagged-perl` key maps to official
stable CPAN String::Tagged 0.24. Its HTTPS release tarball SHA-256
`a3d9ba61af5a419fa4ca40cd084a62642b4ef6533cc42a209f8f7f63e21d74a9`
matches the publisher's `CHECKSUMS`. All 41 archive entries lie under one
root and are regular files or directories, without traversal or links.

The archived `LICENSE` explicitly grants the Perl 5 GPL-1.0-or-later or
Artistic-1.0-Perl terms; the module header repeats the dual-license grant.
This resolves the frozen inventory's historical `license-blocked` flag for
this release rather than treating the flag as an exemption. The official
openEuler 24.03 LTS SP3 RVA23 `everything` primary metadata (compressed
SHA-256 `fdb1663ee6c803e8efcc83c19b7a1548f047f08abba8a52f5fe623b222064d1a`,
open SHA-256 `57be74ba1e5023e98fc645095923f23a3260c3a11c3f4785d89eac353749e84a`)
has neither `perl-String-Tagged` nor `perl(String::Tagged)`; its
`perl(Module::Build)`, `perl(Test2::V0)` and `perl(Test::Pod)` providers
are present. A future generation must be checked again before merger.

Unmodified upstream `./Build test` ran all 22 default `t/` files and 228
assertions locally without skips, including `t/99pod.t` because Test::Pod
was installed. A source-level staged install yielded both modules, the
Formatting POD and three man pages listed in the SPEC. Installed-RPM smoke
checks generated Provides, version, tagged range lookup and mutation.
Target RPM build, complete default test and installed smoke remain for
exact-head CI to verify; PR artifacts alone do not prove public repository
publication.
