<!-- SPDX-License-Identifier: Apache-2.0 -->
# libfile-inplace-perl

The frozen inventory's exact `libfile-inplace-perl` key maps to the latest
official [File-Inplace 0.20](https://metacpan.org/dist/File-Inplace). The
CPAN `CHECKSUMS` entry and downloaded HTTPS archive both have SHA-256
`00d63cf15fdd03a166ecb7af2813a684251254f992fcf5da722ff557b4f10a3e`.
The archive's 15 entries form one top-level tree, with no traversal paths,
links or special files. The module POD and README grant redistribution under
the same terms as Perl; they cite different historic Perl 5 versions but
both allow later Perl 5 terms. The RPM uses the repository's established
`GPL-1.0-or-later OR Artistic-1.0-Perl` expression for this dual license.

The official openEuler 24.03 LTS SP3 RVA23 `everything` primary metadata,
`primary.xml.zst` SHA-256
`fdb1663ee6c803e8efcc83c19b7a1548f047f08abba8a52f5fe623b222064d1a`,
contains neither `perl-File-Inplace` nor `perl(File::Inplace)`. This is a
snapshot check, not a guarantee about future state.

`%check` keeps the only default upstream test file and all 21 assertions.
That test writes temporary edit and backup fixtures within the fresh build
source tree. It passed on local Perl 5.34.1. Target CI must still prove the
RVA23 QEMU result. The installed-RPM smoke verifies an edit and backup in
an automatically cleaned temporary directory.

Successful PR CI artifacts alone do not prove public RPM repository publication.
