<!-- SPDX-License-Identifier: Apache-2.0 -->
# libarray-intspan-perl

This package maps the frozen inventory's exact `libarray-intspan-perl` key
to the official [Array-IntSpan 2.004](https://metacpan.org/dist/Array-IntSpan)
stable CPAN release. The official CPAN `CHECKSUMS` SHA-256 and an
independent HTTPS download agree on
`4dcd17afce0955ee6b2a9bdd6e06669b9fa1daca161e11b4808f0e33a0ce0c99`.
The archive has one top-level tree, only regular files and directories, and
no traversal paths. Its LICENSE and source headers state Artistic-2.0.
CI verifies the pinned source before building for openEuler 24.03 LTS SP3
riscv64/RVA23.

The SHA-256-verified official target Everything primary metadata contains
neither a `perl-Array-IntSpan` RPM nor `perl(Array::IntSpan)` provider.
This target check is separate from the inventory's Ubuntu discovery record.

`%check` runs all eight registered upstream `t/*.t` files. A clean local
pure-Perl run passed all 178 assertions. The installed-RPM smoke checks
integer-range lookup and update behavior plus all three modules. Target
dependency resolution, complete RPM/QEMU tests, and installation require
exact-head CI. PR CI artifacts do not establish public RPM publication.
