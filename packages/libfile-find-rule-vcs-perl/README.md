<!-- SPDX-License-Identifier: Apache-2.0 -->
# libfile-find-rule-vcs-perl

The frozen inventory's exact `libfile-find-rule-vcs-perl` key maps to the
official [File-Find-Rule-VCS 1.09](https://metacpan.org/dist/File-Find-Rule-VCS)
release. The HTTPS source archive and its CPAN `CHECKSUMS` entry both report
SHA-256 `43c798bff0a1f6ac196cfa0f28eddac768954df2d02a04d01974a8fafeafbb49`.
Its archive entries remain under one top-level tree, without traversal paths,
links or special files. The included `LICENSE` explicitly grants Perl 5's
GPL-1.0-or-later or Artistic License terms.

The official openEuler 24.03 LTS SP3 RVA23 `everything` primary metadata,
`primary.xml.zst` SHA-256
`fdb1663ee6c803e8efcc83c19b7a1548f047f08abba8a52f5fe623b222064d1a`,
has neither a `perl-File-Find-Rule-VCS` RPM nor a
`perl(File::Find::Rule::VCS)` provider. Required `perl-File-Find-Rule` 0.34
and `perl-Text-Glob` 0.11 are present. This snapshot check does not guarantee
future repository contents.

`%check` retains all three default upstream test files. They passed 12
assertions on local Perl 5.34.1. The target CI must still prove the complete
QEMU test run. The installed-RPM smoke creates a temporary tree and verifies
that the `ignore_git` rule omits `.git/config` while keeping an ordinary file.

Successful PR CI artifacts alone do not prove public RPM repository publication.
