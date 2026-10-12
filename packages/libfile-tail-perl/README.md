<!-- SPDX-License-Identifier: Apache-2.0 -->
# libfile-tail-perl

The frozen inventory's exact `libfile-tail-perl` key maps to official stable
[File-Tail 1.3](https://metacpan.org/dist/File-Tail) (`META.json`
`release_status: stable`). The official CPAN `CHECKSUMS` entry and downloaded
HTTPS archive both have SHA-256
`26d09f81836e43eae40028d5283fe5620fe6fe6278bf3eb8eb600c48ec34afc7`.
Its 15 entries form one top-level tree without traversal paths, links or
special files. Bundled README/META and the Ubuntu distribution copyright file
identify Perl GPL/Artistic terms for the full upstream release.

The official openEuler 24.03 LTS SP3 RVA23 `everything` primary metadata,
`primary.xml.zst` SHA-256
`fdb1663ee6c803e8efcc83c19b7a1548f047f08abba8a52f5fe623b222064d1a`,
contains neither `perl-File-Tail` nor `perl(File::Tail)`. FileHandle,
File::stat, IO::Seekable and Time::HiRes are available. This is a snapshot
check, not a guarantee about future repository state.

`%check` retains all three default upstream files. They create and remove
PID-named files only in the fresh CI source tree. They exercise file polling,
rotation and name changes, so exact target CI is required to determine whether
timing under QEMU is adequate. The installed-RPM smoke reads a prefilled
temporary file through File::Tail without waiting for future writes.

Successful PR CI artifacts alone do not prove public RPM repository publication.
