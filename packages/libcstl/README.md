<!-- SPDX-License-Identifier: Apache-2.0 -->
# libcstl

Official stable v2.3.0, activesys/libcstl commit
`f0fd5ccb817192614588915ab0b5dbebbc6ed58b`. The fixed archive SHA-256 is
`e415e42a8feff347213d3bdcf61578e3583e876b64d65f96909647f7fa8f7c6a`.
All 475 regular Git files match the archive, with no gitlinks or omitted files.
Historical discovery is `discovery-20260808T165000Z-9a89920c269462cd`, AUR
libcstl 2.3.0-2; that stale recipe was never executed and does not establish
the official release's freshness or build success.

Library source and installed headers carry LGPL-2.1-or-later notices.
COPYING.LESSER and AUTHORS are installed unchanged. Generated Autotools
helpers retain their own license notices/exceptions in the complete SRPM
archive. Original packaging is Apache-2.0; all five patches are LGPL-2.1-or-later.
No upstream write has been made.

The original default configure choices, shared/static libraries and complete
Automake `make check` suite (`TESTS = libcstl_ut`) are retained. All original
test cases and assertions are retained. The first patch enables Automake's
cross-directory object layout, detects the archiver with AM_PROG_AR before
Libtool initialization, places the same test library after objects
in LDADD, and forwards legacy `google/cmockery.h`
includes to the official target's `cmockery/cmockery.h`. It does not replace
cmockery with cmocka's API, drop tests or suppress assertions. Remove it when
upstream supports those layouts. It also makes the original string-array
test's byte-range pointer conversions explicit for GCC 14, matching the
adjacent container test without changing the addresses or ten-element range.
This fixes a real `%check` compilation error, not a RISC-V runtime failure;
strict compiler options remain enabled. The complete original suite must pass CI.

The subsequent exact-head CI run 38725148883 reached another original test:
the list string node passed its generic byte buffer to a string_t cleanup
parameter. The patch now makes the string-object view explicit in the four
list/hash/AVL/RB node cleanup calls and the three matching string accessors,
following the existing list accessor. Only pointer views change: all original
allocations, values, assertions and cleanup calls remain. This is a source
type-compatibility repair, not evidence of a target runtime pass. No compiler
diagnostic is suppressed; replacement exact-head CI remains required.

Exact-head CI 38733504844 then reached the original char-pointer sentinel
`char* str = 0x1111`, rejected by GCC 14's `-Wint-conversion`. The second
patch explicitly types the same hexadecimal pointer sentinels in four original
test sources, including pointer-valued varargs and comparisons. It follows the
adjacent `(void*)0xcc` case; every sentinel value, test case, assertion and
operation is preserved. The first patch is byte-for-byte unchanged. This is
test source type compatibility, not evidence of a target runtime pass; the
complete original suite and downstream consumers still require replacement
exact-head remote CI. No diagnostic, default feature or test is disabled.

Exact-head CI 38741530253 exposed two more original test argument errors.
The third patch passes the allocated basic-string object to the
invalid-pby-string assertion, rather than the address of its local pointer,
and explicitly views the same ten string objects through the range helper's
declared byte-pointer interface. All assertions, values, allocations, cleanup
and registered tests remain unchanged; the first two patches are unchanged.
This corrects original test source types, not a target runtime pass.

Exact-head CI 38747774662 reached the representation tests. The fourth
patch supplies a real initialized char-string type-info pointer instead of
a type-style enum in the null-representation negative test. The representation
remains NULL, preserving the original first assertion under test, and the
fixture is destroyed afterward. The round-trip test views the same `prep+1`
address through the API's declared const-byte-pointer interface. Both original
assertions and registered cases remain; no compiler diagnostic is suppressed.
The first three patches are unchanged. Replacement target CI is still required.

Exact-head CI 38758358457 reached the original function-test pointer arrays.
The fifth patch explicitly casts the 108 nonzero hexadecimal integer
sentinels to void pointers in the six original cases. It preserves all
120 array values, including the 12 NULL constants, all comparisons, algorithm
calls, registered cases, assertions and strict compiler diagnostics. The
first four patches are unchanged. This is generic test source compatibility,
not a RISC-V runtime pass; replacement full target CI remains required.

Separate downstream consumer checks exercise vector/list creation, empty
state, values, size and destruction against staged shared/static and actual
RPM-installed shared/static libraries. They are not upstream tests.
Installation checks validate owned library resolution, package integrity,
license material and the installed consumer's SHA-256.

Target: openEuler 24.03 LTS SP3, riscv64/RVA23 and the immutable image lock.
Dependencies include official libcmocka-devel providing the actual
libcmockery compatibility library. Full primary/filelists namespace and
dependency-name closure were reviewed. Actual DNF constraints, cmockery ABI
compatibility and all original tests remain remote CI gates. Local checks
cover metadata, inert patch syntax, trusted repository tests and SHA-256
only: no local RPM/QEMU/upstream build or native/merge/publication claim.
