<!-- SPDX-License-Identifier: Apache-2.0 -->
# libfile-treecreate-perl

The frozen inventory's exact `libfile-treecreate-perl` key maps to the latest
official [File-TreeCreate 0.0.1](https://metacpan.org/dist/File-TreeCreate).
The official CPAN `CHECKSUMS` entry and downloaded HTTPS archive both have
SHA-256 `57686f10843be81affad185ae4131790ba0c4af36d2104d6fb69126528055267`.
The archive has one top-level tree, no traversal paths, links or special files,
and contains an explicit MIT `LICENSE` file. This resolves the frozen
automated `unverified-upstream` decision for this release.

The official openEuler 24.03 LTS SP3 RVA23 `everything` primary metadata,
`primary.xml.zst` SHA-256
`fdb1663ee6c803e8efcc83c19b7a1548f047f08abba8a52f5fe623b222064d1a`,
contains neither `perl-File-TreeCreate` nor `perl(File::TreeCreate)`. This is
a snapshot check, not a guarantee about future repository state.

`%check` retains both default upstream tests: the compile test (one assertion)
and the tree creation test (22 assertions). They create only relative fixtures
inside the fresh CI source tree and remove them on success. The installed-RPM
smoke creates a temporary tree, checks its contents and removes only that tree.
The full upstream suite also passed locally on Perl 5.34.1; target compatibility
is not claimed until exact-head CI.

Successful PR CI artifacts alone do not prove public RPM repository publication.
