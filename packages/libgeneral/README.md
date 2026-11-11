<!-- SPDX-License-Identifier: Apache-2.0 -->
# libgeneral

Official stable release 90, tihmstar/libgeneral commit
`81e4636784f1bc3fda6a90911fc15bf529975577`. Fixed archive SHA-256:
`afdb4e58495d6791de65e4f9babe9e0af56e855b1a0fc417850651a99953e8ea`.
All 33 regular Git files match the archive, with no omitted files or gitlinks.
Release 90 is officially published, non-draft and non-prerelease; the number
is upstream's Git commit count, not an invented semantic version. Historical
discovery snapshot discovery-20260808T165000Z-9a89920c269462cd contains
libgeneral 90-1 and libgeneral-git 83.r0.g2c3cce0-1. Those are lineage only;
no external recipe or release binary was executed or reused.

The full upstream root LICENSE is GNU LGPL version 2.1, preserved verbatim
in the RPM and full SRPM source. All original copyright notices remain.
Use LGPL-2.1-only conservatively: no separate grant of later versions was
identified. Original packaging is Apache-2.0; the source patch LGPL-2.1-only.
No upstream write was made.

Preserve the full default build: exception, Event, GuardAccess, Manager,
Mem and Utils, all nine public headers, cleanup behavior, shared/static
libraries, normal debug packages and assertions. No minimal/extras switch
is passed. The sole patch stamps five Git queries with the fixed official
release identity because archives contain no .git, and omits Libtool-only
-no-undefined from Linux pkg-config consumer flags while retaining -lpthread
and the original library build flags. Remove when upstream supports archive
versioning and compiler-usable consumer flags.

The original Automake make check target stays enabled; upstream registers no
test cases. Separately labelled downstream checks cover buffer copy/move,
append/resize, decimal/hex conversion, event state with no blocked waiters,
exception metadata/copy and temporary-file round trips. All public headers
compile. The fixture runs with staged shared/static and installed shared/static
libraries; validate pkg-config, owned library resolution, fixture SHA-256,
license material and RPM integrity. These are not upstream-suite or native
concurrency/performance claims.

CI run 38734790860 at head 32104cd14975d669d0b290f77bdc48ba38ce227e
built both original libraries and completed the original make check target,
then failed compiling the separately downstream fixture: its variable name
`error(...)` collided with the public function-like logging macro in macros.h.
Rename only that fixture variable to `fixtureException`; preserve the public
macro, library sources, every fixture assertion and strict compiler options.
This is a packaging-test naming repair, not an upstream or RISC-V source defect.
Replacement target build/install evidence must come from the new head's CI.

Target: openEuler 24.03 LTS SP3 riscv64/RVA23 and immutable ci/image.lock.
Full official 18503/supplemental 1232 primary/filelists joins found no
namespace/file collision; dependency-name/EQ closure is available. Non-EQ RPM
constraints and actual DNF remain CI gates. Local work is inert review,
digest checks and trusted repository validation: no local upstream compile/run,
RPM/QEMU execution, target build/install success, merge or publication claim.
