<!-- SPDX-License-Identifier: Apache-2.0 -->
# libgff

Official COMBINE-lab/libgff v2.0.1, fixed commit
`112721772d5c118f8ddf059395e88057b00067e6`; archive SHA-256
`6f91228d0f3783b0bda4279c4093384e6fbbdb9a1645d732d935192fe66ec501`.
All 25 original Git files are present and blob-verified, with no submodules
or omitted files. Historical AUR/Debian/Ubuntu discovery is lineage only.

The complete original BoostLicense.txt is retained verbatim, including its
literal bracketed derivative-work wording. No additional per-file license
or copyright notice was found. Upstream describes its GFFRead/GCLib origin;
all source remains in the SRPM. Packaging is Apache-2.0; the layout patch is
BSL-1.0. No upstream write has been made.

Keep the default static library and original TestGFFParse program, C++14,
flags, public headers and code unchanged. Retain original index checks by
avoiding CMake's release-specific NDEBUG flag. Upstream registers no CTest
suite and supplies no fixtures. Our explicitly downstream GTF/empty/usage fixtures
exercise its unmodified default program, a staged static consumer, and two
RPM-installed static consumers (direct and CMake). These are not an upstream
unit-test suite. Every check must pass with no ignored errors or skips.

The only patch honors CMAKE_INSTALL_LIBDIR for the archive and CMake metadata
using GNUInstallDirs; it preserves the flat header API. Upstream's v2.0.1 tag
still declares CMake/config version 2.0.0. Preserve that upstream value and
verify find_package(libgff 2.0), without claiming 2.0.1 CMake-version support.

Full target primary/filelists joins found no package/capability or installed
path collision across 18,503 official and 1,232 supplemental packages. Build
dependency names and exact-EQ capability closure are available; literal
version bounds were reviewed, with one versionless libxcrypt-static provider
not asserted to satisfy its versioned requirement. Actual target DNF, build,
parser results and installed ownership remain remote exact-head CI gates.

Target: openEuler 24.03 LTS SP3, riscv64/RVA23, pinned image lock. Local work
only verifies fixed source, inert patch/recipe, metadata and trusted repository
tests; no local upstream/RPM/QEMU execution or native/merge/publication claim.

Initial target CI 38726897124 passed the original build and both eight-check
source/staged fixture phases, then failed packaging with an empty debuginfo
file list: only the static archive was installed. Retain the original default
TestGFFParse ELF in /usr/libexec/libgff, owned by the main package. Keep RPM's
normal debuginfo/debugsource processing enabled, rather than disabling it or
inventing a shared-library target. The installed smoke test also runs all
eight downstream fixtures against that original executable. Existing direct
and CMake consumers remain unchanged. The replacement exact-head build,
installed checks and physical RPM/SRPM products still require remote CI.
