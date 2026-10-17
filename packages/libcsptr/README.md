# libcsptr 2.0.4

Official Snaipe/libcsptr stable v2.0.4 is fixed at
`82d3b1beafe7ed9f13f75e0d3367c60205e10f27` (annotated tag
`998ab7b53314c1d1d2edc07f9d5f0005659b4d38`). All 30 Git blobs, executable
modes and complete archive contents match. The tag and commit are unsigned;
no available detached archive signature was found, and no cryptographic
signature success is claimed.

## Defaults and checks

The original static `csptr` archive, five public headers and manual page stay
enabled. `TESTS=ON`, `SENTINEL=ON`, `FIXED_ALLOCATOR=OFF`, original GNU99/
`-Wall -Wextra -Werror -g` flags, default coverage settings and all original
test bodies/assertions and four named groups remain intact; only Check
registration types and array construction are adapted. The recipe requires Check and
checks the CTest registry is exactly one `check_unit`, so missing Check or an
empty CTest registry cannot silently pass. All twelve original Check cases
run with assertions enabled. The installed runner verifies hashes of the
registration-adapted inputs and replays all twelve cases against installed headers/static archive.

Additional downstream checks cover both shared-array constructors, values,
array dimensions, custom metadata, exact destructor order/count, no early
destruction after releasing the first reference, final destruction exactly
once per element, and unchanged unique-array destructor metadata semantics.
These checks supplement, not replace, the original suite. They are not an
upstream test suite or a performance benchmark.

## Scoped patches

1. Honor GNUInstallDirs for the original archive, with relative `lib64`.
2. Public `shared_ptr(array)`/`shared_arr` set `SHARED | ARRAY`; two equality
   checks incorrectly rejected/skipped reference counting for that kind.
   Bit tests preserve scalar semantics. Array destruction now gets its
   metadata through the existing header-size-aware `get_smart_ptr_meta`
   rather than reading a shared reference counter as array dimensions.
   The array destructor still receives its original array metadata header,
   with caller metadata immediately after it, not a changed API argument.
3. Materialize separate installed QA from this package's tests through the
   repository's actual declared-source/patch staging contract. No original
   upstream test body is changed.
4. Check 0.15.2 defines START_TEST names as const TTest descriptor pointers,
   not legacy TFun functions. The first target build compiled the static
   library but rejected the legacy file-scope TFun registration arrays.
   Construct descriptor arrays inside four group functions, then register
   them immediately with the original group names/order. All twelve
   START_TEST/END_TEST bodies and assertions are byte-identical; the same
   adapted registration and full original bodies run at CTest, staged and
   installed replay. No warning, default, case, assertion or feature is
   disabled. This is a causal fix candidate, not a claim that replacement
   target CI or installed acceptance has already passed.

The default package has only a static archive, so no nonexistent separate
ELF debuginfo subpackage is requested. Original debug/optimization compiler
flags are retained; this is not disabling compilation diagnostics or tests.

## Legal scope

Core library/API, tests and original Coveralls modules retain their complete
MIT notices. FindCheck explicitly grants New BSD terms but omits its named
companion file. The complete AUTHOR-form BSD three-clause companion is
provided as fixed official libssh Git blob
`4b417765f3a834ce6b0a216f6b6c0fe2d3f0bed5` from commit
`07430deb9b97b751ec5ea5a7fc307f40bf042e0a`; the original Daniel Gollub/Bjoern
Ricks notices are retained alongside it. Official Check 0.15.2's finder also
documents the same original opensync provenance and explicit grant. This
fixed legal-text provenance is not libssh code admission or verification of
libssh's separately signed release tag. The unused source auxiliary
`m4/ax_prefix_config_h.m4` retains GPL3-or-later and its original Autoconf
macro exception, accompanied by the complete official GNU GPL3 text. It
does not change the MIT library/API into GPL code. The SPDX expression is
the distributed source/legal scope, not a claim that every binary has every
listed license.

## Acceptance boundary

Official fixed-source/source-only checks and target supply metadata are not
RISC-V build/install results. No local upstream/RPM/QEMU execution is used.
Hosted target CI must prove full original tests, installed replay, downstream
regression, ordinary RPM installation and physical RPM/SRPM acceptance.
The metadata screen does not substitute for DNF dependency solving.
