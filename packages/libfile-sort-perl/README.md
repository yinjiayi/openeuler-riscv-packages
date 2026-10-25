<!-- SPDX-License-Identifier: Apache-2.0 -->
# libfile-sort-perl

The frozen inventory's exact `libfile-sort-perl` key maps to official latest
[File-Sort 1.01](https://metacpan.org/dist/File-Sort). The CPAN `CHECKSUMS`
entry and downloaded HTTPS archive both have SHA-256
`f1bf27c5fa98973632f4d43ba951cda23e84d23b3e1b1b514f0aa56c1c3c532c`.
Its eight entries form one top-level tree without traversal paths, links or
special files. The bundled `README` and `Sort.pm` grant Perl GPL/Artistic
terms, resolving the frozen automated `license-blocked` flag for this release.

The official openEuler 24.03 LTS SP3 RVA23 `everything` primary metadata,
`primary.xml.zst` SHA-256
`fdb1663ee6c803e8efcc83c19b7a1548f047f08abba8a52f5fe623b222064d1a`,
contains neither `perl-File-Sort` nor `perl(File::Sort)`. This is a snapshot
check, not a guarantee about future repository state.

`%check` retains the complete upstream `test.pl`: eight TAP assertions across
file, reverse, numeric and multi-input sorting. It writes relative scratch
files only in the fresh CI source tree and cleans them on success. The
installed-RPM smoke sorts a three-line temporary file. This legacy release's
target-Perl compatibility is not claimed until exact-head CI.

Successful PR CI artifacts alone do not prove public RPM repository publication.
