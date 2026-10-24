<!-- SPDX-License-Identifier: Apache-2.0 -->
# libgcroots 0.3.2

Official uim/libgcroots tag `0.3.2` is fixed to commit
`d362356cc4c5f591695d2fbda7746918250c9e99`, tree
`e3389a2f312d7a005c49f860355a86fa17f8e154`; all 40 regular Git files match
the archive, with no Git submodules or unsafe archive members. SHA-256 is
`006b3e26338f7cf949e51d5bb8d8d20e7211607864e301d72139cb359f11fbac`.
No detached signature is supplied. Frozen Fedora `0.3.2-14.fc44` in
discovery-20260808T165000Z-9a89920c269462cd is discovery lineage only.

The installed library/header use the retained-notice
[Boehm-GC permission](https://spdx.org/licenses/Boehm-GC.html).
Source-only `m4/ax_cflags_gcc_option.m4` is GPL-3.0-or-later WITH
[Autoconf-exception-macro](https://spdx.org/licenses/Autoconf-exception-macro.html),
not Autoconf-exception-3.0 or its generic exception. `ax_func_getcontext.m4`
permits copying/distribution with or without modification while retaining
notices: `LicenseRef-Getcontext-Permission` denotes its exact notice, not an
unsupported claim that its missing warranty text matches FSFAP. Both full
macro files/notices, COPYING and official full GPL3 text are installed.
Source1 GPL3 SHA-256:
`3972dc9744f6499f0f9b2dbf76696f2ae7ad8af9b23dde66d6af86c9dfb36986`.
The SRPM retains original source/notices. No upstream source is modified;
no modification notice is required for it.

Root acquisition is not a complete garbage collector. Only non-threaded
contexts entered through GCROOTS_call_with_gc_ready_stack are supported;
full-system stack scanning and threading are neither added nor claimed.
Upstream already detects RISC-V/Linux and uses __riscv_xlen and its generic
register-save path. No speculative architecture patch is needed. Preserve
the public header's original 0.3.0/API1 macros; configure/pkg-config report
release 0.3.2. These values describe different upstream interfaces.

Original TESTS/check_PROGRAMS are empty. Retain make check and upstream CI's
make distcheck, all configure probes/defaults; do not report these as a
passing original semantic suite. A separate downstream fixture checks
allocator failure, context lifecycle/nesting, return propagation, callback
bounds covering an address-taken stack root and a root value in the scanned
snapshot. It keeps a value live across mark in RISC-V s2, but does not prove
that this value exists exclusively in a register. Positive is_protected is
an API check, not independent root-provenance proof. Run O0/O2 and shared/static
linking (three rounds each), in staged and installed RPM environments with
assertions, SHA-256 and actual shared-link path checks. These are functional
snapshot checks, not full-GC, threading, native hardware or performance evidence.

Fresh full official/supplemental primary/filelists joins found no name,
capability, SONAME, header or pkg-config collision, and a build-root metadata
provider closure. This does not substitute for CI's DNF transaction.
Target build/install/semantic results require exact-head locked
openEuler24.03LTSSP3/riscv64/RVA23 remote CI. Source-only and repository tests
are not target/native success. No local upstream/RPM/QEMU execution,
Auto-merge, upstream write or publication claim.

External source and patch licenses remain those of their respective upstream projects. The repository license only covers original packaging metadata, scripts, and documentation.
