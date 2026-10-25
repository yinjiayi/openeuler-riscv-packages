<!-- SPDX-License-Identifier: Apache-2.0 -->
# libenv

Official Libenv 1.0.3.1, ISC (2025 Mattias Andrée), fixed Codeberg release archive.
SHA-256: `17c49b55aec49277e0d99e27417d5e4327a5c359f13fcf7e73c3e68f41e5541e`.
Frozen discovery: `discovery-20260808T165000Z-9a89920c269462cd`, actual AUR
`libenv` 1.0.3.1-1 lineage; no PKGBUILD execution or upstream writes.

The original default static/shared libraries and both unfiltered `make check`
drivers are retained. Install relocates upstream `/usr/lib/libenv.*` to the
target `/usr/lib64`; all public headers and original manual aliases remain.
Runtime SONAME/ABI is upstream `libenv.so.1` / full library `libenv.so.1.0`,
not the source release number. No dependency or default feature was removed.

The ISC downstream patch makes `va_end` reachable in nine variadic wrappers,
saving each result before ending its argument list. It is a portable C
lifetime fix, not RISC-V-specific. Remove when a fixed official release
passes the unchanged and downstream tests. No upstream submission is made.

The exact original archive is retained in `libenv-tests`; staged and installed
checks each replay unchanged `test.c` and `test-variables.c` with static and
shared linkage. The synthetic original driver supplies its own table symbol;
other functions resolve from the packaged library. Upstream `test.c` has an
unreachable const-list CHECK branch (`else if (dealloc_version)`); its source
is not changed and this gap is not described as original coverage. Separate
consumers exercise all 19 public APIs against the production table, including
const and deallocating ownership, variadic and va_list calls, AND filtering,
OR selection, empty/unknown classes, names versus assignments, stable order,
NULL inputs, and chosen-list allocation. Assertions stay enabled.

Local validation covers recipe metadata, patch dry-run and tooling tests only;
no upstream source, RPM or QEMU executes locally. Real protected CI build,
normal install, original/default tests and physical RPM/SRPM acceptance are
still required before an explicit squash. Variable classifications are not
a security-policy, privilege-transition, native RISC-V or performance proof.

Original packaging is Apache-2.0; upstream source and this source patch remain
ISC. Every subpackage retains the complete ISC notice.
