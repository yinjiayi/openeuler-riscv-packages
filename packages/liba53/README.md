<!-- SPDX-License-Identifier: Apache-2.0 -->
# liba53

This directory packages liba53 `4.0.0` for openEuler 24.03 LTS SP3 on
`riscv64`/RVA23. The official annotated `v4.0.0` tag resolves to commit
`efe146ece29c986c975398da92dd5e53f6319e0a`; its commit-pinned HTTPS
archive has SHA-256
`393521397deb1b3984ce5cc5133d8562f829d49b89e0ad1c70f77716881a253b`.
It is single-rooted and contains only regular files and directories. Source
headers specify GPL version 2 or later; `COPYING` contains GPL-2.0.

The upstream Makefile hard-codes `/usr/lib` and build flags. The spec compiles
the same source set using target hardening flags, produces `liba53.so.1`, and
installs a public C++ header and pkg-config file. The AUR entry provides
discovery lineage only; no AUR recipe was read or executed.

Upstream leaves its fixture targets commented out, while `a53test` returns
zero even on mismatches. `%check` builds and runs the four shipped vector
programs, compares three `.ok` fixtures exactly, and explicitly checks the
18 A5/3 output blocks. The built-in timing line is not used as a performance
claim. Installed-RPM smoke checks a public A5/3 vector through the shipped
shared library. These deterministic vectors are functional tests, not a
security certification.

Exact-head CI run `36434062116` compiled the library and the A5 and KASUMI
fixtures but found that the GEA fixture passes an `int` to an enum parameter
under the C++ compiler selected by upstream's Makefile. The local patch casts
the existing 0/1 direction values to the declared enum, preserving all nine
GEA vectors and their `.ok` comparison. The repaired build remains subject to
a new exact-head CI run.

The first patch-format revision failed in `%prep` on run `36435881975`
because GNU `patch --fuzz=0` could not apply its context, although the native
macOS `patch` accepted it. The replacement patch has been checked explicitly
with GNU `patch --fuzz=0` against the pinned source archive; no fixture or
build result is counted as passed from that failed run.

The upstream source retains GPL-2.0-or-later terms; Apache-2.0 covers the
original packaging metadata, test, and documentation here.
