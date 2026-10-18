# Bioparser 3.1.0

Fixed target: openEuler 24.03 LTS SP3, riscv64, RVA23. Official unsigned tag
3.1.0 resolves to 4fa7126293d2a0eb90125b58fb704f0eed33ffe0. Source0 SHA-256:
a91ac8a14d03d4c87eef4f1a07cd92ab4af82abf5f39b3986019eacbc9630d29.
All 37 Git files and archive modes were verified; no signature is claimed.

## Original defaults and tests

Bioparser is a header-only C++11-minimum library for FASTA, FASTQ, MHAP, PAF
and SAM, including compressed inputs. Both original top-level install/tests
options remain ON. All six original test translation units, 35 cases and ten
plain/gzip fixtures are retained byte-for-byte. The upstream build has no
CTest registration: mandatory check runs its actual original test executable
and verifies a complete 35-case GoogleTest XML result with no failures/skips.
No upstream feature, source file, test body or expected result is modified.

The upstream default test fallback embeds Biosoup 0.11.0. Source1 pins its
official unsigned commit 3e31aa1d9039a2689241aebd18c45933b2d0f5e3 and SHA-256
625a0a0636675a46d1ec1cb3b4c822198f77b9b07e94844b0b196418a8075166.
All 22 Git files are verified. Its original subproject install/tests defaults
remain OFF; no option is disabled downstream. This is Bioparser's normal
test dependency, not onboarding of a separate Biosoup package or evidence
that Biosoup's own timing-sensitive suite passed. Biosoup's independent
timer validation needs native RISC-V; Bioparser's 35 tests contain no timing
bounds. Fixed offline FetchContent input and required system GoogleTest
prevent build-time downloads. Zlib and GoogleTest version requirements remain.

## Installed acceptance

Installed replay means rebuilding the exact six original test sources using
the installed Bioparser CMake target, not source-tree header copies. Private
Biosoup headers and all fixtures are in the tests subpackage. The QA CMake
project rejects an unexpected imported include path. It runs all 35 cases,
then an independent plain/gzip/reset consumer. Installed mode first runs RPM
verification; staged mode is additional check, not installed acceptance.

No ELF is shipped: public payload is six headers and CMake metadata; QA ships
source and data only and recompiles in a fresh temporary directory. Therefore
there is no debug payload to split, although target test compilation keeps
debug information and assertions. Source/private dependency licenses and
per-file copyright notices are retained. SHA256SUMS detects staged/installed
changes, not independent authenticity.

Pre-PR source-only and repository-tool validation do not establish target
build, original-suite execution, ordinary all-RPM DNF installation, actual
RPM namespace safety or physical RPM/SRPM acceptance. Those gates are
mandatory at the exact current head and main before explicit squash.
