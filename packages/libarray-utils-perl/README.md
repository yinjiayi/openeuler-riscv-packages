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
source POD is the license evidence. CI verifies the pinned source before
building for openEuler 24.03 LTS SP3 riscv64/RVA23.

The SHA-256-verified official target Everything primary metadata contains
neither a `perl-Array-Utils` RPM nor a `perl(Array::Utils)` provider. This
target check is distinct from the inventory's Ubuntu discovery record.

`%check` runs the one complete upstream `t/*.t` file. A clean local
MakeMaker build passed all 17 assertions. The installed-RPM smoke checks
unique, intersection, and array-minus operations, sorting sets where
iteration order is not an API promise. Target RPM/QEMU and DNF installation
require exact-head CI. PR CI artifacts do not establish public publication.
