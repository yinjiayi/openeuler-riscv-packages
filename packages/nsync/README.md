# nsync 1.30.0

Review-only proposal, not package or target acceptance. Source capture receipt
`0827077867b244d909f0ec404360246aa971ebd457dbf65438f7088917e863b9`
binds the observed Google repository tag 1.30.0 and all 315 original files/modes.
The annotated tag says “Version 1.30.0”; VERSION and CMake agree. There are no
formal releases. Both selected tag and commit have unsigned/null-signature
fields; that is not an independent cryptographic attestation or a global
signature-absence claim. The calculated archive SHA-256 is
`bb9b1823f6246afd7e7a78497c43ffca62970c94cfebe39c3d58d3a70850a7bd`.

The complete Apache-2.0 LICENSE, all 164 Google source notices, 82 associated
nonempty build/docs files and 68 empty original files are preserved. Installed
source-notices retain all 315 original byte strings, not a replacement blanket
notice. Owned packaging and QA are Apache-2.0 under the same complete text.
The nonempty original x86 dependency file lists paths, not copied system headers.
After the snapshot, exactly one CMake file is patched: its whole-file SHA is
`8ced83088589b9796a4015b9b3e466b86291d7de115fed06e1d7929901e2565c`. A complete 315-entry expected post-patch manifest
changes only that entry; the other 314 original files and all original notice
copies stay unchanged. Both manifests are checked, rather than calling the
patched tree wholly original. The patch is general, not RISC-V-specific, and
remains unsubmitted upstream.

The supported upstream CMake route retains default static libnsync.a and
libnsync_cpp.a, all 13 public headers, and both original CMake export prefixes.
It does not invent a .pc, shared-library default, CLI, or ConfigVersion file.
One package-local CMake export patch makes the existing C++ ABI definitions
PUBLIC, with a downstream modification comment. The producer uses
std::atomic<uint32_t> for nsync_once; without exported definitions a stock
client instead declares uint32_t. That is a static C++ parameter-type mismatch,
not an executed ABI failure or CVE. No private producer-macro override is added
to the positive consumer. Unrecognized
RISC-V CMake architecture uses existing conservative POSIX cputype/compiler
atomics; the source assembly profiles remain unchanged but are not selected.

Default NSYNC_ENABLE_TESTS stays ON. All 26 unfiltered CTest invocations run once.
Each language has 44 TEST_RUN declarations; the two pingpong invocations have
zero default functional subtests because they only declare nondefault
benchmarks. No -s/-x/-m, benchmark forcing, threshold changes or test skipping
are introduced. Timing/scheduler-sensitive original assertions and the
upstream uniprocessor heuristic are retained. Target CI must establish actual
results; elapsed times are not performance, scalability or native memory-model
claims. CMake tests, rather than the separate make test -b route, are used as
documented upstream. Their different benchmark defaults are explicit.

Additive build and installed C and C++ consumers exercise six deterministic API
groups each. The installed baseline uses stock find_package(nsync[_cpp] CONFIG)
and the exported target, with no manual producer macros or include override.
Staged build-root QA alone adds its staged include directory to avoid host SDK
leakage. GNU link trace and map must both same-file bind the selected installed
archive. The C++ consumer statically checks the exported once type. Negative
controls copy actual imported usage requirements (no hardcoded mode macros),
verify identical export-usage bytes, and omit only the archive. They require
relevant undefined symbols and no
executable. Raw command outputs/maps/export usage, ELF/symbol checks, helper/program SHA
bindings and before/after SDK/license/QA hashes are retained even on failure.
Generated export files are measured target outputs, not pretended source SHAs.

This draft has not compiled or executed source. Fresh complete semantic aliases
(nsync/libnsync/google-nsync), target command/dependency and prospective owned
namespace closure, root rights/default acceptance, factory preview+atomic
creation, repository497/source-verify gates and target build/install proof are
still required. Source JSON authority is not inferred from a catalog version.
Raw Arch/openSUSE discovery labels map only to schema arch-core and
opensuse-tumbleweed; observed publisher tags drive the supported numeric
update feed, not a claim of full Daily coverage.

## N240 owned waitable-pointer correction (target verification pending)

Exact head b491c2dea845936f306a3fcfc0933be8709aa17a, Package CI
40575912213 attempt1, passed all 26 original CTests in 156.38 seconds, then
the added C consumer exited with signal status -11. Its captured stdout and
stderr were empty; buffered output does not prove that any earlier owned
group passed. The C++ owned consumer and installed smoke were not reached.
Capture receipt
5e432a923389dfeb88fc0ae498e4c8a78d515ffc57ca46a3bcb2fc800b809801
retains the actual failed build/smoke ZIPs and inner log.

Owned group6 incorrectly put the addresses of the local opaque-handle
variables into the waitable objects. The actual implementation casts each
void pointer directly to nsync_note or nsync_counter. Its own note.c249 and
counter.c98 wrappers, and testing/wait_test.c65/76, pass the handles themselves.
The nsync_waiter.h38-40 illustration contradicts those implementations/tests:
it uses addresses of the handle variables. The original source/header notices
remain unchanged; no upstream patch or documentation rewrite is introduced.

The only executable-text correction removes those two address-of operators
in the embedded owned consumer. Both language profiles, all six groups,
the ready-counter index1 oracle, deadlines, output, assertions, imported targets,
archive/link-map binding and negative omitted-library controls are preserved.
The existing one-hunk C++ export patch and all 315 source-notice bytes are
unchanged, as are all 26 original CTests and source/dependency declarations.
This is a package-owned QA API-usage correction, not an ISA/native defect,
a library implementation fix, a verified replacement-target result or proof
of the exact crashing instruction. No local C/compiler/RPM/QEMU or source-test
execution was performed; the new exact head must establish recovery.
