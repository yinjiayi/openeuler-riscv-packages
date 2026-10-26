# libhat-trie 0.1.2

The source is the official dcjones/hat-trie commit
`6dfc9ed82b188e9ba9b6d8a8bef21fef46416e11`, bound to every one of its 27
ordinary Git members and archive SHA256. The maintainer's annotated `v0.1.2`
tag says “Version 0.1.2”; `configure.ac` declares 0.1.2. This is the versioned
release selected from genuine Debian/Ubuntu frozen lineage, not a claim that
GitHub has a formal 0.1.2 release object: its sole older formal release is
0.1.1. Neither selected tag nor commit offers a signature in the captured
objects. The full commit source URL and digest are pinned in `sources.yaml`.

## Rights and original notices

All 27 original files, including hidden/empty members, are snapshotted before
patches or autoreconf as `license-notices/<relative>.notice`, with SHA256SUMS.
The Daniel C. Jones project COPYING contains affirmative permission and the
inclusion condition, but its disclaimer ends abruptly after “IN”. It is
retained verbatim, not silently replaced by a canonical MIT text; this scope is
`LicenseRef-hat-trie-MIT-truncated`. Paul Hsieh's complete BSD-3-Clause grant in
`pstdint.h` is separate. The original portable-endian and MurmurHash3 public
domain declarations are retained. New QA C code has a complete ISC grant. SPEC and shell packaging are
Apache-2.0 under the repository policy; the derived patch retains the exact
upstream project grant rather than claiming canonical MIT. The complete fixed
official Apache-2.0 text is also shipped for the original packaging material;
it does not replace any upstream grant.

The SuperFastHash derivative in `test/str_map.c` is not licensed by borrowing
the pstdint grant. The original source links Paul Hsieh's official hash page;
that page currently additionally offers the code displayed there under LGPL
2.1, explicitly not every other archive/listing. This package elects the
LGPL-2.1-only branch for that derivative. Apart from renaming the function, the
fork changes the length argument from int to size_t and removes signed-char
casts in the one/three-byte tail cases. The precise attribution/modification
notice and unmodified GNU LGPL-2.1 text are installed. This is not a claim of
historical license timing or byte-identical code. The private author HTML is
evidence only and is not redistributed by this recipe.

## Defaults, narrow repairs and tests

The original default is static-only (`AC_DISABLE_SHARED`). The package retains
the `.a`, `.la`, all five headers in `/usr/include/hat-trie`, and
`hat-trie-0.1.pc`. It does not synthesize a shared variant to claim loader
bindings. A generic local patch preserves caller CFLAGS after upstream's
normal/debug flags, repairs the pkg-config include path/link flag, and resets
stale cardinality/threshold state in the two clear functions. Remove the patch
when an upstream release supplies equivalent repairs/regressions.

The original `make check` builds `check_ahtable`, `check_hattrie`, and
`bench_sorted_iter`, but executes only the first two registered programs.
No tests, random workloads, features or default targets are removed or
reseeded. The benchmark is built, not run or counted as performance evidence.
Both check mains can print failure diagnostics and still exit zero, so the
recipe also rejects their actual error/non-ASCII-failure markers and checks
their Automake PASS records. An original deletion loop's index typo limits
what its nominal iteration count proves; no inflated coverage claim is made.

Six added asserted cases cover nonempty create/overwrite/missing keys,
explicit-length NUL/high-bit binary keys, exact sorted/unsorted iteration,
delete status/cardinality/pointer payload, populated trie clear/reinsert, and
array-table file roundtrip/clear state. No pointer into mutable library storage
is retained across mutations; iterator values are read-only. The original
empty-key get/tryget behavior is inconsistent and is not represented as fixed
or validated by these nonempty-key cases.

The build runs those cases against the built static archive. Installed smoke
uses the installed pkg-config cflags/libs to compile the same consumer in the
target environment, then requires the linker trace/map to identify the same
installed archive, checks archive/consumer symbols and RISC-V ELF identity,
requires an omitted-library negative link to fail with the six actual missing
symbol diagnostics and no output executable, compares exact six-case output
with empty stderr, and checks before/after
archive hashes. Compiler/binutils/pkg-config dependencies are explicit runtime
requirements for this installed-source test. This is static-consumer evidence,
not dynamic LD_DEBUG binding. The installed file manifest is generated after
RPM install-post; original notices and full legal text are checked separately.

All preparation here is inert source review. No local upstream compilation,
tests, RPM or QEMU execution establishes target success. Real target build,
both original checks, installed consumer, full product rights/namespace and
publication acceptance remain separate required gates; optimized unaligned
accesses are not silently disabled to make a RISC-V claim.
