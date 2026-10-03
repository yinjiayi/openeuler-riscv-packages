<!-- SPDX-License-Identifier: Apache-2.0 -->
# libtext-patch-perl

The frozen inventory contains Ubuntu `libtext-patch-perl` 1.8-3 lineage.
The official [CPAN Text-Patch 1.8 release](https://metacpan.org/dist/Text-Patch)
has a 12,652-byte HTTPS archive SHA-256
`eaf18e61ba6a3e143846a7cc66f08ce58a0c4fbda92acb31aede25cb3b5c3dcc`,
matching its publisher `CHECKSUMS` entry. All ten archive entries are inside one
top-level tree and are regular files or directories, with no traversal, links,
or special files. The README identifies the included `COPYING` as the GPL
license text; no included file states contradictory redistribution terms.

The checksum-bound official openEuler 24.03 LTS SP3 RVA23 `everything`
`primary.xml.zst` SHA-256
`fdb1663ee6c803e8efcc83c19b7a1548f047f08abba8a52f5fe623b222064d1a`
has neither `perl-Text-Patch` nor `perl(Text::Patch)`. It supplies
`perl(Text::Diff)` 1.45 and the required core/build/test providers. This is a
snapshot check, not a guarantee about later repository content.

The unmodified upstream `%check` reports one passing test, but `t/test.t`
explicitly exits after a placeholder assertion and disables its substantive
cases because of a historical Text::Diff newline issue. Therefore that result
is **not** treated as feature coverage. The installed-RPM smoke verifies a
real unified patch and preservation of the input string. Context/old-style
behavior and broader newline cases remain unverified. Target QEMU build,
installed smoke, and RPM/SRPM artifacts must be proved by the exact PR head's
CI. A successful PR artifact is not a publicly published RPM or SRPM.
