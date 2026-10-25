<!-- SPDX-License-Identifier: Apache-2.0 -->
# libarray-group-perl

This package maps the frozen inventory's exact `libarray-group-perl` key
to the official [Array-Group 4.2](https://metacpan.org/dist/Array-Group)
CPAN release. The official CPAN `CHECKSUMS` SHA-256 and an independent HTTPS
download agree on `393053cf98f9be9132c9739175b739f426ee81f4dd3e7f8470cbc5ff9e5a1681`.
The archive has one top-level tree, only regular files and directories, and
no traversal paths. The README and module POD grant the same GPL/Artistic
choice as Perl; there is no separate LICENSE file. CI verifies the pinned
source before building for openEuler 24.03 LTS SP3 riscv64/RVA23.

The SHA-256-verified official target Everything primary metadata contains
neither a `perl-Array-Group` RPM nor a `perl(Array::Group)` provider. This
target check is distinct from the frozen inventory's external Ubuntu
discovery record.

The upstream default suite has one file and nine assertions covering row
grouping, class-method usage, and interleaved grouping. `%check` runs it
unchanged. The installed-RPM smoke checks both grouping modes and exact
results. Local pure-Perl tests passed on macOS, but only exact-head CI can
establish the target RPM/QEMU result. PR CI artifacts do not establish public
RPM repository publication.
