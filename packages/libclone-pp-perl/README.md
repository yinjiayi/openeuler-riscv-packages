<!-- SPDX-License-Identifier: Apache-2.0 -->
# libclone-pp-perl

The frozen inventory's `libclone-pp-perl` key records Debian 1.08-2 lineage.
Official CPAN now publishes [Clone-PP 1.09](https://metacpan.org/dist/Clone-PP),
whose 9,619-byte HTTPS archive SHA-256
`4bb44697ef82105bd8d6204e550796a1eea89ce7108a98e0b7bf3ae4700d1c34`
matches the publisher's `CHECKSUMS` entry. All 20 archive entries are inside
one top-level tree and are regular files or directories, with no traversal,
links, or special files. The README and module POD grant use, modification,
and redistribution of the software under Perl's terms; they acknowledge the
historical Ref.pm-derived and Clone-interface portions, and no included file
has a conflicting notice.

The checksum-bound official openEuler 24.03 LTS SP3 RVA23 `everything`
`primary.xml.zst` (SHA-256
`fdb1663ee6c803e8efcc83c19b7a1548f047f08abba8a52f5fe623b222064d1a`)
has neither `perl-Clone-PP` nor `perl(Clone::PP)`. It supplies the required
Perl, MakeMaker, Benchmark, Data::Dumper, and Test::More providers. This is a
snapshot check, not a guarantee about future repository content.

`%check` retains all seven default upstream test files. Local Perl 5.34.1
reported Files=7/Tests=48/Result=PASS; two `t/dclone.t` diagnostics remain
upstream TODOs for its documented reference-to-hash-element limitation and
are not represented as fixed behavior. The target QEMU build and installed
RPM smoke must be proved by the exact PR head's CI. A successful PR artifact
alone is not a publicly published RPM or SRPM.
