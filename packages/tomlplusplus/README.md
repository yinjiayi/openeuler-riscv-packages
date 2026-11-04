# tomlplusplus 3.4.0

One header-only TOML C++17 SDK package for the fixed openEuler riscv64/RVA23
policy. Source is the official formal v3.4.0 release124987467, fixed commit
30172438cee64926dc41fdd9c11fb3ba5b2ba9de and tree
f566f1b23e28cc6afcb9a124ad5422282c3a8156. The original fixed-commit archive is
1,294,825 bytes, SHA256
8874014da21de8d1414d9914c8f3c6b5f315c23a75951b33df46048c13dda12f.
No tag/commit/release asset signature was offered. Raw source is not normalized:
168 files match Git bytes,44 Windows project files have exact forward/inverse
CRLF attribute proofs totaling5,396 pairs; all212 member paths/modes are bound.
The fixed official latest/ref/fullrelease source fence is retained separately.

## Rights

All212 original source bytes are copied into installed source-notices before
build/generation, with a SHA256 manifest. The original complete Mark Gillard
MIT remains separate. Supplemental foreign-notices contains complete Boost1.0,
Hoehrmann MIT, TOML authors MIT and Rebecca Turner ISC fixture grants, fixed
Abseil2017 notice/fullApache2, Niels/Loitsch attributions and the exact Hedley
public-domain dedication. LicenseRef-Hedley-Public-Domain means that preserved
explicit author dedication; it is not a claim of ownership or a substitute
license invented for the bundled source. Own packaging and additive QA use
Apache-2.0 with its full text. Source's generator/CHANGELOG names both test
suites; BurntSushi→toml-lang migration was verified by equal repository ID.
No exact historical fixture-generation snapshot or per-fixture identity is
claimed; current full source-suite grants/credits are retained without an
observed adverse prior restriction. Short generic implementation patterns,
SPDX absence or an ignored UnicodeData filename are not invented license holds.

## Default build and original tests

The production route is unmodified upstream CMake>=3.14, INTERFACE C++17,
BUILD_EXAMPLES=OFF. It installs all52 original include files (51 API headers
plus original /usr/include/meson.build),2 shared sourcefiles and3 CMake exports.
There is no production ELF, shared/static library, pkg-config file or CLI; no
debug subpackage is fabricated. Generated CMake exports are recorded as actual
install outputs, not claimed byte-identical to original source.

Original CMake registers zero tests. The original Linux CONTRIBUTING route is
Meson debug and release, each with -Ddevel=true. Both full default builds are
retained:29 test sources, all9 registered locale calls per profile, build-only
ODR program,6 examples and2 toml-test tools. This is18 original registered
invocations, not18 new tests. Optional external toml-test runner and developer
single-header regeneration are not claimed executed. Upstream devel warnings
remain errors. Target localedef/glibc-locale-source construct all8 UTF-8 locales
in a private LOCPATH; the original C locale is retained, no locale is skipped.

## Bounded scheduling of original tests

Serial test scheduling means one registered locale subprocess at a time; it
does not increase a test deadline, filter cases or change the source. The
[main run 40525457282, attempt 1](https://github.com/yinjiayi/openeuler-riscv-packages/actions/runs/40525457282/attempts/1)
failed in the original debug-profile tests: all9 locale calls started within
one second and were terminated by Meson after30.71–31.51 seconds. Their
partial Catch2 reports show SIGTERM, not an established parser assertion bug.
The release profile, owned consumers and installed smoke were not reached.

The earlier successful PR run used a host reporting4 CPUs and started these
calls in waves of4; its debug calls completed in11.14–29.14 seconds. The failed
main host reported28 CPUs. Both retained RPM_BUILD_NCPUS=2; the unchanged
shared build-container policy applies a2-CPU quota. Host CPU visibility is
not the container CPU quota, and these observations do not establish CPU
utilization saturation, a native-RISC-V failure or an upstream source defect.

This package-only maintenance proposal explicitly invokes Meson with
`--no-rebuild --num-processes 1 --print-errorlogs` for each original profile.
All9 original locale registrations in both debug and release, their original
30-second per-call deadlines, all53 Catch2 cases per successful call, the
build-only programs, full failure logs, source-byte guards and owned checks
remain mandatory. Introspection additionally asserts each deadline is30.
There is no timeout multiplier, skip, test filter or devel-feature relaxation.
The changed scheduling input is a repair hypothesis, not a verified fix; new
exact-head target build/install and independent main/publication acceptance
remain required. Shared Dashboard collection failures are a separate scope.

## Installed SDK checks

The additive consumer has6 deterministic groups: scalar/absent lookup,
nested/array/UTF-8/quoted keys, int64/numeric boundaries, dates/time/offset,
invalid-TOML diagnostics, mutation/format/parse roundtrip. A fresh real CMake
find_package(tomlplusplus3.4.0 EXACT CONFIG REQUIRED) links only its INTERFACE
target, then target GCC compiles the actual installed headers. Its dependency
file, exact CMake location, ELF64/RISC-V executable and57 production hashes are
checked and retained. A wrong3.4.1 EXACT request must fail with actual3.4.0
version diagnostics and no executable. This is a version negative control,
not an invented missing-library link control for a header-only library.
All6 private QA filenames, helper/program/production SHA before/after and full
raw commands/stdout/stderr/dependency metadata are retained. Original source
and owned tests execute only in target CI; no local C++/RPM/QEMU run is claimed.

## Discovery and remaining gates

Raw frozen catalog row139626 retains Arch, Debian, Fedora, openSUSE and Ubuntu
lineages. Final schema maps arch/extra to arch-extra and opensuse to
opensuse-tumbleweed without editing the
catalog. Existing Sniffercommit Source2 is an explicitly retained build dependency
reference, not a duplicate canonical SDK package. Current source identity,
full dependency/provider/namespace and repository validations precede a PR;
target CI, physical RPM acceptance, exact-head merge and publication are later
independent gates. Update configuration uses official GitHub releases and a
strict numericvX.Y.Z regex; it is not a claim of complete Daily coverage.

Owned QA is staged only in a new packaging-qa directory, never over the original
production CMakeLists.txt. All212 live source hashes are checked after prep,
before build, at check entry and after original tests. An inert write-set model
checks every prep-owned output against the complete original source path set.
