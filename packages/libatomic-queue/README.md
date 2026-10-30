<!-- SPDX-License-Identifier: Apache-2.0 -->
# libatomic-queue

This directory packages upstream `https://github.com/max0x7ba/atomic_queue` version `1.9.4` for openEuler 24.03 LTS SP3 on `riscv64`/RVA23.

External source and patch licenses remain those of their respective upstream projects. The repository license only covers original packaging metadata, scripts, and documentation.

## Source and legal provenance

Official stable release: https://github.com/max0x7ba/atomic_queue/releases/tag/v1.9.4
resolves to `40624b83b1074f34eb4dff6836740f9e2b49ad10`.
The fixed official codeload archive is pinned by SHA-256
`439f19deb70262726b6948118d209e3e8028eca7e60fc18c70b7c5749a1236f4`.
All 51 source files match their complete official recursive Git tree blobs;
there are no submodules, unsafe archive members or bundled executable binaries.
The complete original MIT `LICENSE` (SHA-256
`22e4fce4f072000d810546875f26ad1e8b23fcb942fe0a00c85602eb3626c1bb`)
is preserved in the SRPM and both binary packages. No signed tag or detached
signature was observed; this is fixed-byte/Git-identity verification, not a
signature claim. The frozen Debian 1.6.5-2 and Ubuntu 1.7.1-1 lineage is retained,
while the current official release review resolves old unknown-license/source
catalog triage. No distribution recipe is executed or borrowed.

## Build and test contract

This is a header-only library: all five public headers are installed unchanged,
with the upstream Meson-generated `atomic_queue.pc` under `/usr/share/pkgconfig`.
No shared/static library or CMake package is claimed. The `noarch` designation
describes the shipped headers/text/scripts, not the architecture of compilation;
all compilation and execution gates run in the locked openEuler riscv64/RVA23
CI target. The official provider inventory supplies Meson 1.3.1, Ninja, GCC
14.3.1, Boost 1.83.0 (including Boost.Test), glibc and libstdc++ development
files. Full official plus supplemental primary/filelists dependency closure
and header/pkg-config/CMake/static/libexec namespaces are checked before intake;
the later target DNF transaction remains authoritative for dependency solving.

The unchanged upstream Meson defaults are retained: `tests=true`,
`benchmarks=false`, `benchmarks_min=false`. Both original registered tests run:
the complete `src/tests.cc` Boost.Test suite with its original arguments and
`src/example.cc`. The suite keeps all 16 queue stress instantiations, each with
one million messages per producer, plus move-only, allocator, exception-safety,
capacity, FIFO and remapping checks. Stress sum conservation and example sum
checks are evidence of their original assertions, not a proof that every
possible concurrency schedule is correct. The original workload and assertions
are not reduced, selected or patched; only the Meson wall-time allowance is
expanded for emulation. Upstream optional performance benchmarks and sanitizer
CI variants are not default correctness tests and no performance claim is made.

`%check` then recompiles and runs both complete original programs against
staged installed headers. Installed smoke repeats that replay using the installed
pkg-config metadata. All five installed headers and all three retained original
test files are checked against source-generated SHA-256 records. The replay has
finite fail-closed deadlines (30 minutes for Boost.Test, 10 for the example),
preserves failing work directories and never falls back to source-tree headers.
The separate tests RPM owns these unchanged source files and requires the target
compiler/Boost development packages. All source files and the full license stay
in the SRPM; source archives are not committed to Git.

## RISC-V and acceptance limits

`defs.h` has an explicit `__riscv` cache-line and pause-instruction path; the
fixed source also includes upstream RISC-V cross-CI configuration. No downstream
architecture patch is justified or added (`patches/series` is empty). Functional
tests need threads but no kernel privilege, hardware access, real-time scheduling,
huge pages or network. Native latency, throughput, starvation and hardware memory
ordering claims remain outside this QEMU functional gate. Local work performs
trusted metadata/unit/golden and source-only verification, never local upstream
builds or target execution. RISC-V status stays `unknown` until exact-head hosted
build, RPM installation and committed smoke succeed; physical RPM/SRPM acceptance
and explicit squash merge are separate later gates. Auto-merge remains disabled.
