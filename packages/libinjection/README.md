<!-- SPDX-License-Identifier: Apache-2.0 -->
# libinjection

Libinjection 4.0.0 is a C SQL injection and cross-site scripting parser.
Detection is heuristic, not a complete application security guarantee.
Target: openEuler 24.03 LTS SP3 riscv64/RVA23 through the locked OCI/QEMU CI.

## Identity and redistribution

Canonical component: `github.com-libinjection-libinjection`. Discovery snapshot
`discovery-20260808T165000Z-9a89920c269462cd`, rejection row 137810, retains
Fedora Everything-source `libinjection` 3.10.0-15.fc44 as lineage, not executable
packaging. The historical missing-source hold is resolved with official stable
tag v4.0.0, commit `211782219663f889f471650150df12b623c5766e`, tree
`e65d261e5525228020f5c36934892a469de84050`.

Source: <https://codeload.github.com/libinjection/libinjection/tar.gz/211782219663f889f471650150df12b623c5766e>.
SHA-256: `e9d20004c9c7419ffebab1dc17ac5072de2a9b8e43b1289025082dfcdccd25c0`.
All 761 original regular files match official Git blobs. No archive links or
submodule substitution. The tag/commit provides no verified signature;
official identity and checksum are not a cryptographic signature claim.

The complete original BSD-3-Clause COPYING grants source/binary redistribution
with copyright, conditions and disclaimer retained. Auxiliary files keep their
own notices: GPL-3.0-or-later git-version-gen, GPL-2.0-or-later ar-lib with its
distribution exception, GPL3 ax_compiler_vendor.m4 with its Autoconf output
exception, permissive Libtool/macro notices, X11 install-sh, and the short
permissive unbuilt Go example grant. The fixed archive retains all these files
and notices. Full verbatim GNU GPL2/GPL3 companion texts are additional pinned
sources in the SRPM and license payload. Helpers are not installed as executable
runtime code or silently relicensed BSD/Apache. Language bindings are unbuilt.

Target metadata screening covered 18,503 official and 1,283 supplemental RPM
identities and complete joined filelists: no canonical/SONAME/header/static/
shared/pkg-config/test namespace owner and no missing dependency capability.
This is not a successful DNF transaction. Hosted CI must prepare actual target
dependencies and build offline; no online pip or distro PKGBUILD is executed.

## Original defaults and additional checks

The Git archive lacks distribution-only `.tarball-version`; the recipe supplies
exactly the verified release `4.0.0` to the original version helper before
`autoreconf -i --force`. It retains shared/static defaults and all nine default
programs. The library stays at upstream's O0 default because test_stack_xss.c
explicitly requires no optimization. Assertions stay active; no source patch
or selection is introduced. Only Libtool `.la` install metadata is removed,
not the original static `.a` or any default target.

`make check` runs all six original entries: unit fixtures, SQLi negative/positive
corpora, XSS positive corpus, stack regression and error handling. Original
expected corpus mismatch counts 21/18/20 stay unchanged; these are not allowed
test skips. The error suite conditionally omits two allocation cases on OOM,
so downstream additionally requires all 16 cases to pass. Speed binaries are
built by original all but are not timed by check. Separate style/static
analysis, Valgrind, fuzzing, multi-platform CI and native performance are not
claimed validated by this functional QEMU route.

The tests subpackage retains original drivers/scripts and every original unit
and corpus input with SHA256SUMS. Staged and installed replays recompile the
unchanged drivers against the staged/installed shared library, run all six
original entries and require the full error summary. Two additional consumers
exercise shared pkg-config and the explicit static archive, each with six
semantic assertions. The marker separates these downstream checks from upstream
cases. Installed smoke runs from /tmp and verifies all four RPMs with rpm -V.

Local validation is source-only: repository schema/golden/tooling tests and
pinned source digests. No local upstream configure/make, RPM or QEMU execution.
Exact-head hosted default build/check, real installation, physical RPM/SRPM/ELF
and license acceptance and protected explicit squash are still required.
No target success, Auto-merge or public product acceptance is claimed here.

External source and patch licenses remain those of their respective upstream projects. The repository license only covers original packaging metadata, scripts, and documentation.
