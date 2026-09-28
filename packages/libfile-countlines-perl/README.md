<!-- SPDX-License-Identifier: Apache-2.0 -->
# libfile-countlines-perl

This package maps the frozen inventory's exact `libfile-countlines-perl` key
to official stable CPAN [File-CountLines v0.0.3](https://metacpan.org/dist/File-CountLines).
The RPM version is `0.0.3`; the leading `v` appears only in the upstream
archive name. The HTTPS source SHA-256
`cfd97cce7c9613e4e569d47874a2b5704f1be9eced2f0739c870725694382a62`
matches the official CPAN `CHECKSUMS` index. All 13 archive entries are
regular files or directories under one top-level tree, without traversal.
The module explicitly grants Perl GPL/Artistic redistribution and
modification terms, and declares its examples public domain; this resolves
the frozen discovery record's unverified-license flag with primary evidence.

The official openEuler 24.03 LTS SP3 RVA23 target `primary.xml.zst` SHA-256
`fdb1663ee6c803e8efcc83c19b7a1548f047f08abba8a52f5fe623b222064d1a`
contains neither an RPM named `perl-File-CountLines` nor a
`perl(File::CountLines)` Provide. This checks the repository snapshot, not
future repository state.

`%check` runs both upstream default test files, including the 21-assertion
functional suite and its POD test. The optional upstream Test::Pod dependency
is declared as a BuildRequires so CI can avoid the optional-dependency skip.
An upstream-commented case
for a block size smaller than the separator is not counted as validated.
The installed-RPM smoke checks its Perl auto-Provide and counts newlines in
an isolated temporary file.

Successful PR CI artifacts alone do not prove public RPM repository publication.
