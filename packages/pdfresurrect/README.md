# Pdfresurrect 0.23

The selected official stable tag is v0.23 (commit 7a57bffaa8e0ad47f9b0a4fa44fe5ae621680c62,
tree 198491aa3b22a0af2e6e13bb7f6f0b274e378aca). The complete numeric tag list,
main.h VER and ChangeLog confirm this version; there are no formal GitHub releases.
Source0 is 55,233 bytes, SHA-256 e47a75a328020e4ebac5768921daa50b77c30610e787f0e78139fd4766a970ed.
The archive's 13 original files match Git bytes and executable modes. The one
package-local source patch described below changes only the two configure inputs;
all 13 original byte strings remain installed as raw notices.
The unchanged sources.yaml redistribution reason describes the unmodified raw
archive matching the selected Git tree, not the downstream patched working tree.

The project and manual use BSD-3-Clause. All original authors/notices are retained.
Generated configure contains three separate FSF unlimited-copy/distribute/modify
grants, preserved verbatim in the SRPM and installed source-notices; they are not
relabeled as a guessed SPDX license. The Apache-2.0 text applies to owned packaging
and QA only. Its exact previously verified official legal bytes are supplied as
Source1; the upstream project is not described as Apache-licensed.

The original configure/make-all/install route builds one CLI and supplied manual.
Checked-in configure is invoked with Bash, retaining effective -O3 -Wall alongside
RPM flags. No original test target or fixtures exist, so no fictitious make check
is called. All 13 original source files/modes are verified before patching; after patching,
11 unchanged originals and two exact postpatch byte strings/modes are verified
at prep, before build and at check. All original raw notices remain unchanged.
The original experimental scrub feature remains disabled.

Owned QA adds six semantic groups with ten exact CLI status/stdout/stderr cases:
usage/version; a one-version PDF; incremental two-version/quiet; inline creator
and indirect title strings; extracting both revision selectors plus existing-output
rejection and original preservation; invalid and missing input rejection.
The six deterministic data fixtures have independently checked byte offsets and
classic xrefs; valid files exceed the original 1,023-byte header read requirement.
Extraction copies the full original file then appends a selected startxref trailer.
It does not remove old content, render PDFs, or prove confidential-data scrubbing.
Timeout is failure. Every target invocation records raw outputs, hashes, environment,
cwd, actual CLI/helper identities, ELF64/RISC-V metadata and build-ID. Installed QA
requires the exact /usr/bin/pdfresurrect file; standard RPM stripping is preserved,
so build-role and installed-role ELF hashes are not falsely equated.

No source/compiler/RPM/QEMU execution is performed during inert preparation.
Functional target success, generated debug paths, physical RPM/SRPM acceptance and
full fresh provider/namespace admission remain separate required gates. These
bounded classic-PDF cases do not establish security, performance, comprehensive
PDF compatibility, rendering, native execution or full-Daily coverage.

N244 diagnostic-only follow-up: the initial target run 40607517284/a1 failed
while configure checked whether a compiled C program could run. The build
artifact did not retain config.log, so the underlying cause was unknown at that observation.
The packaging now prints the regular, non-symlink config.log on configure
failure between explicit status-bearing markers, preserving the original
configure arguments and exit status. Missing/read-failed log diagnostics do
not replace that failure status. This is not a source/native-execution fix,
main alignment, successful target build or newly accepted physical product.
Sources, flags, probes, owned QA, test assertions and dependencies are unchanged.

N245 source-flag repair proposal: diagnostic run 40613665527/a1 subsequently
retained config.log between original-status=1 markers. Its cache records the
incoming compiler hardening flags, but configure:2652 invokes gcc with empty
CFLAGS while retaining generic-hardened-ld. The linker reports R_RISCV_HI20 and
fopen R_RISCV_CALL_PLT relocations and exits 1; ./conftest then does not exist.
This is a compiler-probe input mismatch, not evidence of a native/ISA execution
fault or a missing dependency. The final live PR/ref fence of that diagnostic
capture remained incomplete after two retained EOF reads; the immutable ZIP/log
is verified, but a fresh exact-head/history/lease gate is still required.

Patch 0001-preserve-CFLAGS-in-compiler-checks.patch removes only the hand-written
CFLAGS clear and corrects its adjacent comment in configure.ac and checked-in
configure. X save/restore and all Autoconf internal flag tests stay unchanged.
Thus an empty original CFLAGS still reaches the original -O3 -Wall default;
provided RPM flags remain available during probes. No autoreconf, --host,
cache-answer bypass, timeout change, test filtering or hardening removal occurs.
All 13 original raw notices, the original configure argv/status diagnostics,
experimental scrub default, six owned groups and ten exact CLI cases remain.
Patch bytes/SHA and the two postpatch digests are explicit; upstream has not
been contacted. Remove the patch after a reviewed upstream stable source has
equivalent behavior and the unchanged target build/install checks pass.

This is an unverified source repair until the replacement head completes its
own target CI and physical-product gates. Two observed heavy failures and one
remaining configured attempt are retained pending the fresh complete lineage
audit; a new head does not reset the budget. No target run or lease is claimed
by this frozen proposal itself.
