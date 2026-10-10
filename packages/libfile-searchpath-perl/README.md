<!-- SPDX-License-Identifier: Apache-2.0 -->
# libfile-searchpath-perl

The frozen inventory's exact `libfile-searchpath-perl` key maps to official
[File-SearchPath 0.07](https://metacpan.org/dist/File-SearchPath). The CPAN
HTTPS archive and `CHECKSUMS` entry both report SHA-256
`be4a2594ef1a7577e773135add940179c6a324e07e12bcfdc463cb49119a2cb9`.
All 21 archive entries remain under one top-level tree, without traversal
paths, links, or special files. The included `README`, module POD and
`Build.PL` permit redistribution and modification under GPL version 2 or
any later version.

The official openEuler 24.03 LTS SP3 RVA23 `everything` primary metadata,
`primary.xml.zst` SHA-256
`fdb1663ee6c803e8efcc83c19b7a1548f047f08abba8a52f5fe623b222064d1a`,
has neither a `perl-File-SearchPath` RPM nor a `perl(File::SearchPath)`
provider. `perl-Module-Build` and `perl-Test-Simple` are available. Upstream
only recommends `Env::Path`, which is absent from this target snapshot; the
core-Perl environment-path fallback is retained, not patched or skipped.
This snapshot check does not guarantee future repository contents.

`%check` retains the one-file default upstream test suite. All 16 tests
passed on local Perl 5.34.1 without `Env::Path`. The target CI must still
prove the complete QEMU run. The installed-RPM smoke creates a temporary
file and searches for it through a private PATH-like environment variable.

Successful PR CI artifacts alone do not prove public RPM repository publication.
