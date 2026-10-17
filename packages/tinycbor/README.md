# TinyCBOR 7.0

Fixed official `intel/tinycbor` tag `v7.0`, commit
`6442e749ca811e24afad1551338a45c75e09808f`. The lightweight tag and commit
are unsigned; no signature is claimed. Archive SHA-256:
`5e9a9f379bc2378bbc5f4bc9bbf16f3a3f9837393b4520ed061309b92a57a8f4`.
All 66 Git files and executable modes are verified. The official archive has
63 files: three `export-ignore` metadata files are fixed additional Sources
with non-hidden transport basenames and restored to their original dotfile
paths in `%prep`. Its `.tag` is the exact intentional `export-subst` commit
expansion, not altered to the raw Git template.

The MIT license and original per-file Intel/S.Phirsov copyright notices are
retained, including the complete aggregated `UPSTREAM-NOTICES` in every RPM.
The discovery snapshot's old 0.6.1 row was `license-blocked` because its
distribution metadata license was `unknown`, explicitly retained for later
official upstream review. This is not ignored: the fixed official 7.0 LICENSE
(SHA-256 `3c6ba0b5bfa7830505301ffb336a17b0748e0d61c4d34216e9dc98f10e40395e`)
contains the full MIT grant, and all per-file notices were separately audited
and retained. The original historical rejection row remains in admission
evidence; no catalog decision is rewritten by this package PR.
Project/header/pkg-config version is **7.0**; the upstream shared-library
VERSION expression would yield **0.7.0**. These are different fields, not a
reason to rewrite upstream versioning.

Preserve original static library default, floating point, CBOR-to-JSON and
tools ON, freestanding and examples OFF, upstream warnings and optional
`WITH_VALGRIND=ON` detection. No Valgrind execution is claimed if it is absent.
`BUILD_TESTING` has no upstream default assignment: the recipe explicitly
enables all five original suites as upstream CI does. Qt6 Core/Test and cJSON
are mandatory, with exact five-suite registry and json2cbor product checks to
prevent silent omission. The original C90/C++ compile-only tests remain so;
encoder/parser/tojson retain every body, assertion, fixture and data-row skip.
Qt6.5.2's variadic QSKIP accepts/discards the historical SkipSingle argument;
no Qt compatibility patch or removal of the zero/NaN exclusions is needed.

Patch0 changes only two pkg-config paths to GNUInstallDirs full variables;
relative `lib64`/`include` install destinations continue to yield relocatable
CMake exports with the original non-namespaced imported target `tinycbor`.
Patch1 adds packaging QA/notice files only, leaving original source/tests
unchanged. Remove patches when equivalent authenticated upstream integration
exists and all original defaults/tests remain preserved.

`%check` runs the original five CTest commands, including optional upstream
Valgrind wrapping, then replays all five installed test executables. Original
Qt skips are not counted as failures or misrepresented as zero skips.
Independent installed pkg-config/CMake API consumers and a JSON/CBOR CLI
roundtrip are downstream checks, not a substitute or upstream suite. The
upstream-built, not upstream-installed, json2cbor executable is retained under
the tests package's private libexec directory. Normal ELF debug RPMs and
compiler debug flags remain enabled for all installed executables.

Local validation is trusted repository tooling, schema/golden/source-only
checks and inert zero-fuzz GNU patch materialization only. No local upstream
configure, compile, tests, RPM or QEMU execution. RISC-V target CI, ordinary
installation, installed tests and physical RPM/SRPM/debug acceptance remain
required and have not yet been observed for this new package.
