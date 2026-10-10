<!-- SPDX-License-Identifier: Apache-2.0 -->
# jbigkit

This directory packages JBIG-KIT 2.2 for openEuler 24.03 LTS SP3 on
riscv64/RVA23. The frozen discovery lineage records Fedora 44, Arch stable,
Debian stable, openSUSE Tumbleweed and Ubuntu's then-current 2.1 versions;
these historical records are not evidence of their current releases. AUR was
queried only through read-only RPC for android-riscv64-jbigkit metadata; no
PKGBUILD or install hook was executed.

The [official University of Cambridge release page](https://www.cl.cam.ac.uk/~mgk25/jbigkit/)
announces stable 2.2 (2026-10-09). Its fixed
[release archive](https://www.cl.cam.ac.uk/~mgk25/jbigkit/download/jbigkit-2.2.tar.gz)
is 441594 bytes, SHA-256
`3302109c93b7befbffa3cfe8bceb4355f19dea0ee7dcb5f33710b1648bf6645c`.
Archive inspection found one jbigkit-2.2 root, 50 regular files, and no absolute
path, parent traversal, link or special entry. Source verification is not
target build success or a signature verification claim.

A SONAME is the shared-library name embedded in a linked executable. The SPEC
keeps the existing recipe's `libjbig.so.2.1` and `libjbig85.so.2.1` names through
the separate `jbig_soversion` macro, so a source-version bump does not remove
those names. Static comparison of all three public headers against official
2.1 with this recipe's two backports finds unchanged structure layouts and
function declarations. Differences are comments/whitespace, version macros
and the `JBG_VLENGHT` to `JBG_VLENGTH` inline macro typo fix. This source-level
review is not a compiled binary ABI certification; target CI and artifact
inspection remain required. The installed smoke links both ordinary and
explicit pre-update library names and checks both codec header versions.

The complete upstream `make test` gate remains enabled. It covers the library
T.82/T.85 codec tests and the PBM/JBIG functional round trips. The installed
smoke test adds public API link checks and
a PBM-to-JBIG-to-PBM conversion against the packaged shared libraries. RISC-V
status remains unknown until the pinned openEuler RVA23/QEMU workflow
completes.

The two GPL-2.0-or-later security backports formerly shipped by this recipe
come from Ubuntu's official `2.1-3.1ubuntu0.22.04.1` security source package,
originally authored upstream by Markus Kuhn:

- `0001-cve-2017-9937-limit-decoded-image-size.patch`, SHA-256
  `906b9e9cd9125eda9e62865529874de2fc7192a906b7010d1daff09aa3da9782`.
  Stable 2.2 contains `jbg_dec_state.maxmem`, its 2000000000-byte default and
  the decoded-image `JBG_ENOMEM` limit in `libjbig/jbig.h` and `libjbig/jbig.c`.
- `0002-jbg-newlen-check-marker-length.patch`, SHA-256
  `9fa937db94020724ba8c5946c8c86f277760856923d1e17db62796fdf30c5703`.
  Stable 2.2 contains the `p + 5 >= bie + len` NEWLEN payload guard in
  `jbg_newlen()` before reading its payload.

The official 2.2 `CHANGES` corroborates both fixes. Their previously recorded
removal conditions are fulfilled, so they are retired from SPEC, metadata and
series rather than applied twice; original patch bytes remain recoverable in
Git history. No RISC-V patch is removed. The functional suite still runs
serially because its Makefile shares temporary filenames; no test is skipped.
No upstream compiler, make/test, RPM or QEMU execution was performed locally
for this migration. Only static/source verification and repository tooling
tests were run; new-head target results and publication remain separate gates.

External source licenses remain upstream's. Apache-2.0 covers only this
repository's original packaging metadata, scripts, tests, and documentation.
