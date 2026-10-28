# Pdfresurrect 0.23

The selected official stable tag is v0.23 (commit 7a57bffaa8e0ad47f9b0a4fa44fe5ae621680c62,
tree 198491aa3b22a0af2e6e13bb7f6f0b274e378aca). The complete numeric tag list,
main.h VER and ChangeLog confirm this version; there are no formal GitHub releases.
Source0 is 55,233 bytes, SHA-256 e47a75a328020e4ebac5768921daa50b77c30610e787f0e78139fd4766a970ed.
All 13 original files match Git bytes and executable modes. No source patch is used.

The project and manual use BSD-3-Clause. All original authors/notices are retained.
Generated configure contains three separate FSF unlimited-copy/distribute/modify
grants, preserved verbatim in the SRPM and installed source-notices; they are not
relabeled as a guessed SPDX license. The Apache-2.0 text applies to owned packaging
and QA only. Its exact previously verified official legal bytes are supplied as
Source1; the upstream project is not described as Apache-licensed.

The original configure/make-all/install route builds one CLI and supplied manual.
Checked-in configure is invoked with Bash, retaining effective -O3 -Wall alongside
RPM flags. No original test target or fixtures exist, so no fictitious make check
is called. All 13 original source files/modes are verified before and after build.
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
artifact did not retain config.log, so the underlying cause remains unknown.
The packaging now prints the regular, non-symlink config.log on configure
failure between explicit status-bearing markers, preserving the original
configure arguments and exit status. Missing/read-failed log diagnostics do
not replace that failure status. This is not a source/native-execution fix,
main alignment, successful target build or newly accepted physical product.
Sources, flags, probes, owned QA, test assertions and dependencies are unchanged.
