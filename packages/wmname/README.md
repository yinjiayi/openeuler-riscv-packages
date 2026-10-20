<!-- SPDX-License-Identifier: MIT -->
# wmname

Print or set the X11 EWMH root-window name. Official stable release is 0.1:
https://tools.suckless.org/x/wmname/ and
https://dl.suckless.org/tools/wmname-0.1.tar.gz, SHA-256
`559ad188b2913167dcbb37ecfbb7ed474a7ec4bbcb0129d8d5d08cb9208d02c5`.
All five regular archive members were read; original MIT/X Consortium notices
are retained. The archive is not committed. Upstream supplies no archive
signature. Discovery component `tools.suckless.org-x-wmname` retains arch-extra
and Fedora lineage from snapshot `discovery-20260808T165000Z-9a89920c269462cd`.
No distribution recipe or third-party binary was executed or repackaged.

The original default all/install targets, C99/pedantic/Wall/-Os flags, version
define and Xlib linkage are retained with RPM flags and system paths. Patch1
defers original Makefile stripping to RPM debug processing. Patch2 fixes static
ignoring of XGetWindowProperty bytes_after: the initial 128-byte read is followed
by a full measured read, with UTF8_STRING/8 and completeness validation plus
checked byte-counted output. A missing property still prints nothing; setter
and original version/usage statuses are unchanged. These locally authored MIT
patches are downstream-only, not upstream submissions, and removable when a
stable upstream release provides the corresponding fixes. This is a generic
source issue, not a demonstrated native RISC-V-specific failure.

Upstream declares no check/test target; none is skipped. Separate private-Xvfb
checks run in percent-check and again after ordinary DNF installation. They
check original bytes/notices, version/usage/no-display behavior, missing name,
nine name boundaries (empty, 127/128/129 bytes, long ASCII and UTF-8), supporting
root-window property, and rejection of wrong type/format. These are functional
fixtures, not native display/timing/performance/security or exhaustive EWMH
certification. A fresh isolated X server is created for each invocation.

Target is openEuler 24.03 LTS SP3 riscv64/RVA23 with the immutable repository OCI
image and deterministic offline build dependencies. Target build/install and
actual RPM/SRPM acceptance must come from exact-head CI; local metadata/tooling
validation and source/patch verification alone are not target acceptance.
Auto-merge is not enabled. Fresh protected-main, CI, namespace and physical
product gates remain mandatory before an explicit squash merge.
