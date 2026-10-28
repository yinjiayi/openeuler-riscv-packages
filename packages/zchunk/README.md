# Zchunk 1.5.5

Fixed highest official numeric stable tag `1.5.5`, not a formal GitHub release.
Meson version agrees and README states stable API/ABI additions since1.0.
The annotated tag84e9d1f peels to ae8e9f5b; the archive root uses the tag-object
prefix. All166 files match the peeled commit tree byte-for-byte and by Git mode.
Independent isolated GPG verified both signed Git objects with the current
official linked-author certificate. This is not a detached archive signature.

The deliberate single SDK includes all six original utilities, shared library,
public header/pkgconfig and six supplied manuals. Original feature auto-selection,
tests/docs enabled, shared default and GNU11 remain. All default dependencies are
explicitly supplied; `--wrap-mode=nodownload` prevents network fallback. Meson
buildtype plain consumes RPM flags plus debug information and preserves assertions.
Normal automatic debuginfo/debugsource packages remain enabled; actual generated
debug paths/build IDs and ELF payloads require independent target verification.

All40 original Meson tests on the intended little-endian target remain unfiltered,
with their original expected-negative case and version-dependent zstd checksum
oracles. Upstream's truncated-preface regression returns77 with the exact
"Skipping: needs valgrind or AddressSanitizer" message when no memory checker is
active. The normal tree retains that declared result (or requires its normal OK),
not a fabricated preload or compiler macro. A separate non-installed Meson tree
in .packaging-qa/asan-build uses actual AddressSanitizer instrumentation and must
run all40 unfiltered tests:39OK/1original expected failure/zero skips. Its compiler
commands must contain -fsanitize=address, and both its DSO and original bounds
regression must need libasan.so.8. Existing gcc's exact official runtime closure
supplies libasan; no source or dependency declarations change. Sanitizer options,
leak-disable overrides and LD_PRELOAD are rejected; no sanitized library is
installed. All166 source bytes/modes are checked again after this companion run.
The first target run40628732712/a1 completed38OK/1XFAIL/1declared memory-check
SKIP, then failed the owned post-check assertion; it did not establish memory-test
coverage. This package-only change adds that missing coverage, not an upstream
or native defect fix. ASAN under QEMU is not yet verified and remains a required
fresh-target gate, not a claimed pass. Failure evidence:
https://github.com/yinjiayi/openeuler-riscv-packages/actions/runs/40628732712. The owned six-group QA is additive: six exact CLI versions, zstd/nocomp
binary CLI roundtrips, malformed input, installed public C API roundtrips with exact
same-file DSO/linker-map/trace proof, and a no-library negative link control.
The runner records every raw stdout/stderr/status/argv/cwd/environment and hashes
its own source, production inputs and selected DSO before/after. It does not test
HTTP-server interoperability, exhaustive inputs, security, native ABI or performance.

Project/manual BSD2, buzhash MIT, uthash BSD1, bundled SHA1 public domain/SHA2 BSD3,
and Windows musl MIT/TRE BSD2/dirent MIT retain distinct authors and complete notices.
The unchanged LibreOffice legal compilation remains a separate MPL2 fixture, not
a BSD reassignment or copies of all libraries/fonts merely named in that text.
All166 raw originals/modes remain in SRPM and test inputs. Installed text notices
are exact bytes; non-text records explicitly use reversible base64 plus original
hash/mode. The x86-64 ABI reference is only original SRPM/nondefault ABI-tool data,
never executed or installed as a target ELF. `test-abi`/`new-abi` remain nondefault
manual tools; no native ABI-compliance claim is made. No source patch is proposed.

Official full metadata and current exact-head declarations/provider/namespace gates,
trusted repository validation/497 tests/golden/actionlint/source-only verification,
and real target build/install/smoke/physical checks remain separate acceptance gates.
No local upstream code, compiler, RPM or QEMU execution was used to prepare this.
