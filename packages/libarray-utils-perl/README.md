<!-- SPDX-License-Identifier: Apache-2.0 -->
# libarray-utils-perl

This package maps the frozen inventory's exact `libarray-utils-perl` key
to the official [Array-Utils 0.5](https://metacpan.org/dist/Array-Utils)
CPAN release. The official CPAN `CHECKSUMS` SHA-256 and an independent
HTTPS download agree on
`89dd1b7fcd9b4379492a3a77496e39fe6cd379b773fd03a6b160dd26ede63770`.
The archive has one top-level tree, only regular files and directories,
and no traversal paths. Its `Utils.pm` POD explicitly grants the GPL or
Artistic License choice under the same terms as Perl. It has no separate
LICENSE file; MetaCPAN's structured license field is unknown, so the
source POD is the grant evidence. All seven original files, modes,
MANIFEST entries and the original Sergei Fedorov copyright/warranty and
Laszlo Forro contribution credit are retained unchanged. `%license`
installs the original `Utils.pm` grant plus the full GPL1 and ten-clause
Artistic-1.0-Perl terms from immutable official Perl commit
`76298ae68aa7796f0ffc05095b127d23f4b2de8f`. These pinned text documents
supplement the referenced grant; they do not assert Perl code ancestry,
replace the source or relicense it. No tag-signature or legal-certainty
claim is made. CI verifies all three pinned sources before
building for openEuler 24.03 LTS SP3 riscv64/RVA23.

The SHA-256-verified official target Everything primary metadata contains
neither a `perl-Array-Utils` RPM nor a `perl(Array::Utils)` provider. This
target check is distinct from the inventory's Ubuntu discovery record.

`%check` runs the one complete upstream `t/array-utils.t` file with its
original `no_plan` and all 17 assertions. Each invocation has a 180-second
deadline and a 10-second termination grace. A second whole-suite
Test::Harness invocation requires exactly one file, 17 passes and zero
skips, TODO, unexpected successes or failures; no original test is edited,
excluded or replaced. These counts are static expectations until the
refreshed head's hosted CI confirms them. This refresh executes no upstream
source or target RPM/QEMU locally. The installed-RPM smoke checks
unique, intersection, and array-minus operations, sorting sets where
iteration order is not an API promise. Target RPM/QEMU and DNF installation
require exact-head CI. The old head's successful CI has no retained
artifact and is not product acceptance for this refresh. Fresh complete
CI, schema-valid results and physical RPM/SRPM verification are still
required. PR CI artifacts do not establish public publication.
