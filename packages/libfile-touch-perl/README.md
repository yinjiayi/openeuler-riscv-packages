<!-- SPDX-License-Identifier: Apache-2.0 -->
# libfile-touch-perl

The frozen inventory's exact `libfile-touch-perl` key maps to official stable
[File-Touch 0.12](https://metacpan.org/dist/File-Touch). The official CPAN
`CHECKSUMS` entry and downloaded HTTPS archive both have SHA-256
`2a04dc424df48e98c54556c6045cab026a49e3737aa94a21cf497761b0f2e59c`.
Its 15 entries form one top-level tree without traversal paths, links or
special files. The bundled `LICENSE` grants Perl GPL/Artistic terms.

The official openEuler 24.03 LTS SP3 RVA23 `everything` primary metadata,
`primary.xml.zst` SHA-256
`fdb1663ee6c803e8efcc83c19b7a1548f047f08abba8a52f5fe623b222064d1a`,
contains neither `perl-File-Touch` nor `perl(File::Touch)`; it does provide
the required `perl(Time::HiRes)`. This is a snapshot check, not a guarantee
about future repository state.

`%check` retains both upstream default test files: one module-load assertion
and 18 timestamp assertions. The latter creates and deletes only
`t/example-file.txt` inside the fresh CI source tree. The installed RPM smoke
verifies the Perl auto-Provide and changes an isolated temporary file's mtime.
Exact target results await CI.

Successful PR CI artifacts alone do not prove public RPM repository publication.
