<!-- SPDX-License-Identifier: Apache-2.0 -->
# libarray-diff-perl

This package maps the frozen inventory's exact `libarray-diff-perl` key to
the official [Array-Diff 0.09](https://metacpan.org/dist/Array-Diff) CPAN
release. The official CPAN `CHECKSUMS` SHA-256 and an independent HTTPS
download agree on `8006392e9861e741537c2bbc9116c8e42b962f2e07e8d641a2ff6a11c6445077`.
The archive has one top-level tree, only regular files and directories, and
no traversal paths. Its LICENSE and module POD grant the same GPL/Artistic
choice as Perl. CI verifies the pinned source before building for openEuler
24.03 LTS SP3 riscv64/RVA23.

The SHA-256-verified official target Everything primary metadata contains
neither a `perl-Array-Diff` RPM nor a `perl(Array::Diff)` provider. It does
contain `perl-Algorithm-Diff` (providing `perl(Algorithm::Diff)` 1.201),
`perl-Class-Accessor` (providing `perl(Class::Accessor::Fast)` 0.51), and
the required Test::Pod and Test::Pod::Coverage modules. This target check
is separate from the inventory's external Ubuntu discovery record.

`%check` runs all six upstream `t/*.t` files: the 13 functional assertions
and four POD/POD-coverage files. Both POD dependencies are declared so those
tests cannot silently skip for missing modules. The installed-RPM smoke
checks the module provider and sorted-array added/deleted/count behavior.
The two functional files passed locally; local Test::Pod::Coverage is absent,
so the complete six-file suite and RPM installation require exact-head CI.
PR CI artifacts do not establish public RPM repository publication.
