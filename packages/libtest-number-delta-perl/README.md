<!-- SPDX-License-Identifier: Apache-2.0 -->
# libtest-number-delta-perl

The immutable discovery snapshot
`discovery-20260808T165000Z-9a89920c269462cd` contains the canonical
component `metacpan.org-release-test-number-delta`. Its Debian `stable/main`
lineage records `libtest-number-delta-perl` version `1.06-4`, fetched at
`2026-08-08T16:50:00Z`. This is distinct from the inventory's exact
`libtest-number-delta-perl` key, which contains Ubuntu `resolute/universe`
lineage; that Ubuntu row is not relabelled as Debian evidence.

The [official Debian stable source index](https://deb.debian.org/debian/dists/stable/main/source/Sources.xz)
was independently rechecked against its Release metadata and still contains
source package `libtest-number-delta-perl` version `1.06-4`.
This current confirmation was observed on `2026-10-05` at `22:56 UTC`;
it does not replace the original frozen observation time.
Its upstream homepage and the frozen canonical record identify the official
[CPAN Test-Number-Delta 1.06 release](https://metacpan.org/dist/Test-Number-Delta).
Distribution rows are discovery lineage, not upstream checksum or license proof.
The publisher's `D/DA/DAGOLDEN/CHECKSUMS` and downloaded HTTPS source archive
both give SHA-256
`535430919e6fdf6ce55ff76e9892afccba3b7d4160db45f3ac43b0f92ffcd049`.
The 43 archive entries stay under one top-level directory, without traversal
paths, links or special files. The distribution-wide `LICENSE`, `README`,
and `lib/Test/Number/Delta.pm` explicitly grant Apache-2.0 rights. No
third-party or vendored executable code was found in the archive.

The official openEuler 24.03 LTS SP3 RVA23 `everything` `repomd.xml` pins
`primary.xml.zst` SHA-256
`fdb1663ee6c803e8efcc83c19b7a1548f047f08abba8a52f5fe623b222064d1a`.
That metadata has neither `perl-Test-Number-Delta` nor
`perl(Test::Number::Delta)`, but does provide the required
`perl(Test::Builder)`, `perl(Test::Builder::Tester)`, `perl(Test::More)`,
and core dependencies. This is a repository snapshot, not proof of public
availability at a later time.

`%check` retains all 12 default upstream test files. Hosted target run
`37380981794:1` at commit `21f527bd433f99836f413985ba2fa19d3c006b28`
passed the original 12-file, 72-assertion suite without skips and installed-RPM
smoke; this is evidence for that exact commit, not a replacement head.
The nine separate `xt` author/release tests are outside the default suite
and are not claimed passed. No local upstream execution is claimed by this
repair; each replacement head requires its own complete target CI and artifacts.
The installed smoke checks RPM ownership, module version, passing absolute
tolerance and inequality behavior. PR CI success does not prove publication.

The existing official CPAN directory updater is retained. Its JSON-decoded
regular expression matches the actual official `1.04`, `1.05`, and `1.06`
archive filenames; escaped JSON display is not a reason to unescape it again.
