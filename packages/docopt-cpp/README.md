# Docopt.cpp 0.6.3

One deliberate C++11 shared/static SDK, from formal v0.6.3 and exact commit
42ebcec9dc2c99a1b3a4542787572045763ad196. The tag/commit are unsigned and the
selected release offers no detached archive asset; no signature or key is guessed.
All 18 original Git bytes/modes remain in the SRPM and pre-patch notice snapshots.

Select the explicit whole-port BSL-1.0 choice offered in README.rst. Both full
MIT/Boost grants, original authors' notices and the exact boost::hash_combine
credit are retained. No historical Boost version/author is invented and the
borrowed helper is not claimed to have been blanket MIT-relicensed. The packaging
and owned additive QA are separately Apache-2.0, with the full legal text included.

The narrow two-file patch updates the stale CMake release stamp 0.6.2 to 0.6.3
(SONAME major 0 unchanged), converts only the original Python driver's print
syntax/shebang and wires CTest to that same configured full driver. Defaults
WITH_TESTS/WITH_EXAMPLE/USE_BOOST_REGEX are originally OFF. Packaging explicitly
opts in tests; shared and static libraries, C++11 and standard regex remain.
There are 175 original language-agnostic cases: 142 expected JSON successes and
33 expected errors. The original negative contract accepts nonzero exit, not a
new stronger exact-status claim. No original driver/case is executed locally.

Both CMake imported targets (docopt and docopt_s) and pkgconfig(docopt) are tested
on the target using closed installed/buildroot paths, six additive public API
groups per route (18 functional invocations), same-file linker maps/traces and
loader/ELF evidence, and no-library negative controls. Every static archive
member must be a RISC-V ELF64 relocatable. SDK/legal/QA bytes, modes and symlinks
are snapshotted before/after; complete JSON evidence is emitted into target logs.
The original install does not export/install a complete header-only route, so no
installed DOCOPT_HEADER_ONLY compatibility claim is made or substituted for the
mandatory shared/static routes. No Boost dependency is needed by default stdregex.

Production uses CMAKE_BUILD_TYPE=None with RPM flags and -UNDEBUG. Normal RPM
debuginfo/debugsource generation is retained. No native ABI, performance, target,
physical, merge or publication success is inferred before its actual evidence.

## Target CTest registration repair (2026-10-28)

Initial head 96cde794181bc124cfae59b0348c9223ae40787f, Package CI
40639718318 attempt 1, compiled the SDK and staged it into the RPM buildroot, then failed in %check.
No RPM installation/smoke acceptance was reached.
With CMP0110 unset at the original minimum-policy level, the whitespace-bearing
CTest name became `Testcases` and `docopt` became the executable token. CTest
reported Not Run/exit 8; none of the original 175 cases ran and owned downstream
QA was not reached. This is a downstream wiring error, not evidence of a parser,
exception-type, architecture or native-only defect.

Use the whitespace-free name `docopt-testcases` in the existing metadata patch
and its exact registry assertion. The Python command, complete 175-case driver,
case data, all 18 original notices, SDK, flags and all additive QA are unchanged.
The proposed correction is not target-verified until fresh CI on its new head
passes; no old result or product is transferred.
