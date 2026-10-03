<!-- SPDX-License-Identifier: Apache-2.0 -->
# Devel::StackTrace::AsHTML 0.15

Frozen Debian `libdevel-stacktrace-ashtml-perl` 0.15-2 lineage maps to the
official stable MIYAGAWA CPAN release. The fixed HTTPS source is 17,053 bytes,
SHA-256 `6283dbe2197e2f20009cc4b449997742169cdd951bfc44cbc6e62c2a962d3147`,
matching the publisher's `CHECKSUMS`.

The top-level `LICENSE` grants same-as-Perl redistribution for “This software.”
The release `README` explicitly applies its copyright notice to all files in
the distribution unless stated otherwise; no contrary file notice was found.
The `README` and installed module credit HTML generation copied from
CGI::ExceptionManager by Tokuhiro Matsuno and Kazuho Oku. The earlier official
CGI::ExceptionManager 0.06 archive (SHA-256
`cfb581a5f753d70adb95326491516bdc06912fcb90b4579ceaf741b9b2a1293c`)
names both authors and directly grants that library same-as-Perl rights in
its `README`/module and top-level `LICENSE`. This is a distribution-specific
redistribution assessment, not a claim about unverified personal signatures.

The SHA-bound official openEuler 24.03 LTS SP3 riscv64/RVA23 primary has no
`perl-Devel-StackTrace-AsHTML` name or `perl(Devel::StackTrace::AsHTML)`
provider. It supplies `perl(Devel::StackTrace)` 2.04, `perl(Data::Dumper)`
2.183, `perl(Scalar::Util)` 1.63, MakeMaker 7.70 and Test::More 1.302198.

The unchanged published default suite has seven files: three functional files
with four assertions run, and four author/release-only files self-skip by
upstream design. Local `make test` passed at precisely that scope. Target
`%check` requires all three functional files and exactly those four
self-skips, with no functional skip or hidden assertion loss. Installed smoke
separately verifies HTML rendering and Unicode, ampersand and angle-bracket
escaping. Target exact-head CI must prove physical RPM/SRPM and DNF installed
smoke. No local RPM/QEMU build or publication occurred.
