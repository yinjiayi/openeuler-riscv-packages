<!-- SPDX-License-Identifier: Apache-2.0 -->
# Data::Perl 0.002011

The frozen Ubuntu `libdata-perl-perl` 0.002011-2 key maps to the official
[Data-Perl 0.002011](https://metacpan.org/dist/Data-Perl) CPAN release.
The publisher's `CHECKSUMS` and an independent download of the 23,235-byte
HTTPS archive agree on SHA-256
`8d34dbe314cfa2d99bd9aae546bbde94c38bb05b74b07c89bde1673a6f6c55f4`.
The archive has a single top-level tree, only regular files and directories,
and no traversal paths.

The bundled `LICENSE`, release README, and all fifteen installed PM files
explicitly grant redistribution under Perl 5 terms from copyright holder
Matthew Phillips. The LICENSE spells out GPL version 1 or later or Artistic
1.0. Contributors are credited in the README; no file states conflicting
terms.

The official openEuler 24.03 LTS SP3 riscv64/RVA23 primary contains no
`perl-Data-Perl` RPM or `perl(Data::Perl)`/submodule provider. It uniquely
supplies all hard runtime and test providers, including Role::Tiny,
List::MoreUtils, Test::Deep, Test::Fatal, and Test::Output.

Unmodified upstream `make test` selects all eleven default test files.
Nine functional files pass 194 assertions locally; two author-only POD files
self-skip unless `AUTHOR_TESTING` is set by upstream design. Their optional
Pod::Coverage::TrustPod dependency has no official target provider, so this
package does not claim author-mode POD coverage. Exact-head target CI must
reproduce the nine functional passes and report the two explicit author-only
skips, build physical RPM/SRPM products, install with DNF, and pass the
installed string/array/number wrapper smoke. PR CI does not establish
public RPM publication.
