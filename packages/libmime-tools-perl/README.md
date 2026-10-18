<!-- SPDX-License-Identifier: Apache-2.0 -->
# libmime-tools-perl

This package maps the frozen inventory's exact `libmime-tools-perl` key to
the official [MIME-tools 5.519](https://metacpan.org/dist/MIME-tools) CPAN
release, issued on 22 September 2026. Its HTTPS archive was independently
downloaded and pinned to SHA-256
`2e465205482a4c5938ee3537f215ba22ac96b22c7a42b4f7d32d0f77fa1a49cf`,
which matches the official CPAN `CHECKSUMS` index. The archive contains one
top-level tree, no traversal paths, links, or special files. CI verifies the
pinned digest before building for openEuler 24.03 LTS SP3 `riscv64`/RVA23.

The upstream default suite has 41 `t/*.t` files. `%check` runs it in full,
including the 5.519 concatenated-base64 security regression, the localhost
SMTP test, and gzip/BinHex decoder cases. The spec explicitly installs gzip
and Convert::BinHex so their upstream decoder checks are not silently omitted.
The author-only Kwalitee and opt-in POD coverage checks retain upstream's
conditional behavior; a skipped conditional check is not counted as a pass.
The installed-RPM smoke checks that the package provides MIME::Parser and
MIME::Entity and parses a message entirely in memory.

MIME-tools requires MailTools, which is being onboarded separately in PR
[#2159](https://github.com/yinjiayi/openeuler-riscv-packages/pull/2159).
That dependency must be available to the target CI before this package can
build or install; this PR does not establish that it already is. The module
uses the same GPL/Artistic choice as Perl itself. CI artifacts do not prove
publication to the public RPM repository.
