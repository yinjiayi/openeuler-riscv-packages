<!-- SPDX-License-Identifier: Apache-2.0 -->
# libucontext 1.5.2

This directory packages upstream `https://github.com/kaniini/libucontext` version `1.5.2` for openEuler 24.03 LTS SP3 on `riscv64`/RVA23.

External source and patch licenses remain those of their respective upstream projects. The repository license only covers original packaging metadata, scripts, and documentation.

libucontext implements userspace context creation and switching. This package
uses the existing upstream RISC-V RV64 implementation, not an invented patch.
Target status is unknown until exact-head CI and physical product acceptance.

## Official source

Stable tag `libucontext-1.5.2` resolves to immutable commit
`49e671dd52ff6791295d8161ad3b6da7dc5f6f9d`. The complete official commit archive
SHA-256 is `c84f57298ed4bce278c31ed8e5c0b3da6f9bd8bc45c9dfb08656fe797bdc2c47`.
All 131 files match that official Git tree, with safe relative paths and no links.
The lightweight tag was read back unchanged. No detached archive signature was
published on the inspected official release/tag surface; none is claimed verified.

Frozen discovery `discovery-20260808T165000Z-9a89920c269462cd` retains
Arch-extra/Fedora lineage. Their recipes were not copied or executed. Official
NEWS/VERSION and current tags promote the frozen1.5.1 row to stable1.5.2.

## License and notices

Core and architecture source uses an ISC-style permission with the copyright
and permission-notice condition. The original LICENSE plus complete original
architecture/source files are installed as notices, preserving all per-file
holders/years including additional authors and2025 notices. They are copied
before compilation so the license notice tree contains no generated objects.
Original notices remain in the source RPM as well.

`LicenseRef-libucontext-test-public-domain` denotes the explicit `Public domain.`
dedication in both original test sources. The cooperative threading example has
no individual public-domain header and is covered by the repository LICENSE,
not assumed to carry that dedication.
It does not mean inferred CC0, Unlicense, or a grant for unrelated source. Complete
original notices for these files are installed with the core notices.

## Defaults and validation

Original GNU make `all` and `check` are retained, with explicit `ARCH=riscv64`,
compiler/packaging flags and installation paths. FREESTANDING=no,
EXPORT_UNPREFIXED=yes, BUILD_POSIX=yes and hard-float defaults are unchanged.
Both shared/static libraries, headers and pkg-config metadata are included. The
optional scdoc documentation build is not an upstream default and is not enabled;
the unchanged manual source is packaged as documentation.

All three default make-check test variants are retained, with unchanged sources.
Installed smoke reruns their installed ELFs and asserts actual glibc loader
bindings to these packaged libraries, not a libc-only successful ABI call.
Upstream's POSIX link order may select its own bare weak aliases. After preserving
that behavior, a fourth invocation of the same POSIX test explicitly preloads
the packaged POSIX library and requires getcontext/setcontext/swapcontext bindings
to that library. This is functional testing, not native timing or performance.

RV64 register-layout assertions are retained; default user-context/FPU operations
and ordinary signal-mask calls do not require a privileged kernel or hardware
performance claim. Actual QEMU limitations must be reported honestly.

## Admission and acceptance boundaries

Build: bash, binutils, coreutils, gcc, glibc-devel, grep, make, sed.
Explicit runtime: bash, coreutils, grep plus automatic ELF dependencies.
Fresh official RVA23 repomd binds18503 primary/filelist identities and2207942
paths. Static declared closure contains61 packages/32versioned edges, with no
missing root/transitive provider or official name/path conflict. It is not a DNF
SAT-solver result and establishes no supplemental-repository freshness.

The recipe requests unprivileged execution and needs no undeclared network fetch;
this is not proof of container network isolation. Actual trusted CI uses a
network-enabled bridge and rechecks the source-cache checksum. The metadata flag
network_during_build=false describes the recipe requirement, not CI isolation.
Local metadata, trusted tooling tests and checksum-only source verification are
not local source QA/RPM/QEMU builds. Real exact-head CI, installation/smoke and
physical products remain acceptance gates. No patches, remote writes, commit or
push were performed by the independent intake lane; auto-merge is not enabled.
