# Jshon 20131105

Canonical component github.com-keenerd-jshon is the official upstream JSON
command-line tool. Discovery aliases and 20180209 development snapshots are
lineage only: this recipe deliberately selects the latest official stable tag
20131105, commit ed54be6b1396f9024137cd1e9148c9329b80d7e4. Its fixed tag archive
has SHA-256 28420f6f02c6b762732898692cc0b0795cfe1a59fbfb24e67b80f332cf6d4fa2.
All six original source members were reviewed inertly. The original full MIT
notice is retained in source and both installed packages. No detached archive
signature is advertised; SHA-256 is not an independent maintainer signature.

The original Makefile builds the default executable and installs its manual.
All original -std=c99 -Wall -pedantic -Wextra -Werror flags remain, extended
with RPM optflags, not overridden. The stable release contains no completion
file (the development snapshot's unrelated _pbpst destination is not imported)
and no declared check/test target. We do not invent an upstream test pass.
The reported original --version stays 20131105 and matches the package.

One package-local MIT patch fixes input handling: initialize empty stream data,
terminate regular-file reads, reject fopen/read failure before dereference,
and return immediately for empty JSONP data before constructing a pointer
before the buffer. The file-read fixes are backported from the official
d919aeaece37962251dbe6c1ee50f0028a5c90e4 source; the two empty guards are
locally authored. No upstream write or upstream acceptance is claimed.
Remove the patch when a stable release includes equivalent guards and the
same regressions pass. It does not alter valid-input parser defaults or
hide warnings. This is a source correctness fix, not a RISC-V-specific patch.

Downstream staged and normally installed checks cover the original manual's
type/length/keys/extract/across/history/insert/delete/by-value/JSONP/sort/NUL
operations, original version, UTF-8, pipe/file/large input, in-place editing,
and invalid input. MALLOC_PERTURB_=165 makes missing input initialization
observable on target glibc; checks keep the original empty-input warning
policy and use -Q explicitly when silence is requested. Original source,
manual and license bytes remain independently hash-bound in the QA archive.
The package has no exhaustive parser, fuzz, memory-safety, security, native
hardware or performance certification. Target build/install and physical
RPM/SRPM acceptance remain mandatory before merge; local tooling is not that
acceptance. No upstream build or target QEMU/RPM is executed locally.

Full current official and supplemental primary/filelists admission checks
providers and projected owned paths; actual DNF solving remains a CI gate.

The first target CI rejected the original patch in `%prep`: the final unified
hunk was not portable to GNU patch despite a successful BSD patch dry-run.
The patch is regenerated from the exact stable source with complete standard
context and counted hunks. GNU patch now applies all five intended input
guards with `--fuzz=0` and zero offsets; required blank context markers are
retained. This repairs patch formatting, not the parser, QA or warning policy.
No original check is removed and replacement target CI remains mandatory.

The next target run passed patch application and the original warning-strict
build, then exposed an incorrect downstream invalid-option expectation.
The original `-Q` changes Jshon's own quiet flag, not libc `getopt`'s default
diagnostics. The invalid-option test is retained and now requires exit status 2,
empty stdout and the exact C-locale diagnostic including executable path.
Other quiet checks and all input regressions remain unchanged; stderr is not
ignored and no source/default behavior is altered by this QA-only correction.
