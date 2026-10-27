# libe131 1.4.0

This package uses the official non-prerelease v1.4.0 release asset, published
2018-05-14, rather than a distribution's `1.4.0+repack` archive. The fixed
captured commit is `56899c0504e00b78741ff6f8ac7b4d749bc7eb23`, tree
`14a958b56522af383f9e8b986b909de93b265f47`. Source SHA-256 is
`3937ca6253b348788d8eaa41b562002e523358b34755bc4eb6353853b3e161d6`.
The tag/asset URLs remain mutable; this checksum records the captured bytes.
No tag, commit or release-asset signature was offered in the observed source.
No independent publisher signature or guessed sidecar is claimed.

The 23 release files include six exact Git files and 17 generated Autotools
files. All original bytes, including every generated notice/exception, are
copied before packaging changes to `source-notices/<relative>.notice`, with
23-entry SHA256SUMS. The release omits `.gitignore`, `autogen.sh` and two Git
network examples. These omissions are upstream dist behavior, not package
test removal. The four original Git-only files remain in private provenance
evidence but are not silently substituted into the release source.

## Rights and provenance

The project ships its full Apache-2.0 text and Hugo Hromic notices. Source and
header expressly identify work based on forkineye/E131. The complete original
Shelby Merrick2015 custom free-use/credit/disclaimer notices are retained as
`Shelby-Merrick-E131.h.notice` and `.cpp.notice`. They define
`LicenseRef-Shelby-Merrick-E131`; this custom grant is not relabelled as GPL.
Their evidence is fixed upstream commit
`9046a03685d7d12d50ed1269f2494cd8458d2c5b`, Git blobs
`db295d5c1f0f793a8457eb8040012febd9bebca6` and
`af49a3786397aa859ac3ae972151ab3885bb7496`. This is present observed grant and
attribution evidence, not a claim of historical commit/grant attestation.

README's protocol explanations retain their original wiki citation and
project Apache declaration. The cited wiki now redirects to a forum; neither
the original article/license nor a historical wording comparison was
recovered. No unrelated forum content is included. That dead link is not
represented as evidence of a conflicting license or as recovered permission.

Generated helpers retain X11, FSFUL and FSFAP grants, GNU GPL2-or-later or
GPL3-or-later notices and each explicit distribution exception. Where a
literal GPL2-or-later grant permits it, the GPL3-or-later branch is selected.
Full GPL2 and GPL3 texts are also installed. The composite source-distribution
license records these build-helper materials; it does not turn the actual
runtime implementation into a GPL-only library. Original packaging and the
added consumer are Apache-2.0, with the full text already present in original
LICENSE. Three source inputs suffice: the release plus GPL2/GPL3 texts; an
extra Apache source is not invented or counted.

## Preserved defaults and added QA

The generated configure, original make all/install and both default shared
and static libraries are retained. Libtool version-info is exactly `1:4:0`:
the expected Linux real library is `libe131.so.1.0.4`, SONAME `.so.1`.
The header, static archive and libtool archive are installed. No upstream
pkg-config file exists, so none is invented. Existing RISC-V patterns in
config.guess/sub are preserved; their age alone is not a portability failure.

Original `make check` is always invoked, but its `check-am: all-am` has zero
registered programs or functional cases. Its success is not functional-test
coverage. The two Git-only examples loop indefinitely, use UDP/multicast
and are neither default build nor test targets. No example is called passed.

Six additional cases check packet initialization/wire lengths and invalid
arguments; validator mutations/error strings; option-bit independence; pure
multicast-address formatting/errors; sequence-window/wrap implementation
behavior; and initialized stream-dump/null errors. There is no DNS, live
network, lighting equipment, timing, performance or security-certification
claim. Packet validation is not presented as comprehensive hostile-input
validation. Sequence checks describe the captured implementation, not an
independent E1.31 standards-conformance certification.

Installed smoke recompiles the consumer only from installed source/header
and `-le131`, with no ambient include/library overrides or RPATH. A strict
missing-library control must fail with all nine relevant unresolved symbols
and no executable. Positive output equals all six exact case lines plus
summary, with empty normal stderr. ELF64/RISC-V, SONAME/DT_NEEDED and all nine
normal loader bindings are mandatory; caller and target use same-file `-ef`
against the actual consumer and versioned installed library, not spelling
assumptions about `/lib64` aliases. Raw compiler/ELF/nm/stdout/stderr/loader
chunks and digests are emitted on success/failure. Library/archive/header
digests are compared before/after. The installed manifest is generated after
RPM install-post stripping, at the end of `%check`.

Only target CI may establish compile/build/install/QA success. Locally the
source is inertly inspected and repository validation/source verification
may run; no local upstream compilation, RPM or QEMU run is authorized.
Full provider/namespace projection is separate from DNF SAT and from actual
RPM/automatic debug-output physical acceptance. No build-id path is guessed.
The N227 fixed-source/rights/default/provider evidence and actual creation,
gates, commit and PR receipts are private reproducibility records; no shared
catalog release entry or full Daily discovery coverage is invented.
