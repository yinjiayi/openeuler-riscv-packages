<!-- SPDX-License-Identifier: Apache-2.0 -->
# libnewuoa

Official elsid/newuoa-cpp v0.1.2, immutable commit
`8a7d5164a2a9db3756d3e8d5d9b5e67ab2a775f8`. Archive SHA-256
`f9393868cab10d0552ac4d197839f70dc6d20bff18438837614f5e1966cb1e7b`.
All9 archive files match official Git blobs; no detached signature or Git
submodule is supplied. Discovery lineage is the existing August8 libnewuoa
catalog entry, revalidated against all official tags. No AUR recipe executed.

The catalog's generic license-blocked triage is resolved by reading the actual
official full MIT LICENSE and complete MIT grant/notice at the beginning of
src/newuoa.cpp (Powell2004 and AttractiveChaos2008). Both are retained verbatim
in SRPM and installed license files; the latter retains the entire original
source rather than removing notices or manufacturing a license grant.

Retain the default static C++11 library, public C header and original upstream
CMake/pkg-config consumer metadata. No patch or shared-library ABI is claimed.
Upstream registers no test target or CTest tests. Its two original C/C++ examples
are not default CMake targets; both are additionally compiled with assertions
enabled and run unchanged against staged and installed library bytes. Their
illustrative trust radii are not corrected or treated as convergence evidence.

Explicitly downstream numerical checks call all three public APIs: plain C
callback, mutable closure and const closure. Each minimizes a deterministic
two-variable positive-definite quadratic, requires finite output, verifies the
minimum/coordinates within stated tolerances, and requires an observed callback
count between1 and500. Separate direct pkg-config and CMake imported-target
consumers exercise installed metadata. These are small functional checks, not
upstream tests, numerical-method certification, performance or native-hardware
evidence. Original examples/header hashes are checked before each replay.

Only standard compiler/CMake/make/pkgconf target dependencies are needed. Installed
compiler dependencies support repeatable installed consumers; no build-time
network is required. Target is openEuler24.03 LTS SP3 riscv64/RVA23. Local work
is metadata/source-only: real hosted target build/install and independent whole
RPM/SRPM/ELF acceptance remain required before merge. Publication is separate.

Initial exact-head hosted CI38995764240 compiled the static library and passed
both unchanged examples, all three numerical API checks, and both metadata
consumers, then failed while packaging an empty automatic debuginfo subpackage.
This static-only package has no separately installed ELF debuginfo payload, so
its SPEC disables that empty subpackage only. Optimization/debug compilation
flags, the default library, original sources, licensing and every check remain
unchanged. The initial RPM packaging failure is not counted as build/install
success; a new head still requires complete hosted CI and physical acceptance.
