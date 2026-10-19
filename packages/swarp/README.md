<!-- SPDX-License-Identifier: MIT -->
# swarp

This directory packages upstream `https://tools.suckless.org/x/swarp/` version `0.1` for openEuler 24.03 LTS SP3 on `riscv64`/RVA23.

This is suckless Simple Pointer Warp, not the unrelated astronomical image
resampler SWarp. Discovery lineage is `aur:swarp` from the recorded
20260808T165000Z snapshot, used only to find the official project; no AUR recipe
or third-party binary is executed or repackaged. The official release page
still advertises 0.1. Source is the fixed
https://dl.suckless.org/tools/swarp-0.1.tar.gz archive, SHA-256
`ef5730fe8ee00879cbec1e91e22a7f0f7817a63375d790d775f5b7427886d45f`.
All five regular members were inspected; both original MIT/X Consortium
copyright notices are retained. No archive is committed.

The original default `all` and `install` targets, `-Os`, version define,
coordinate parsing and Xlib linkage are retained with target system paths and
RPM hardening/debug flags. The sole downstream Makefile patch defers stripping
to normal RPM processing so debuginfo/debugsource are not lost. It is locally
authored under MIT, not submitted upstream, and removable when a stable
Makefile supports packaging-controlled stripping. Original C is unchanged.

Upstream declares no test/check target. Separate downstream checks run against
the staged tree in `%check` and again after ordinary DNF installation. They
verify the fixed original archive, both licenses, README, exact version/usage
and no-display errors, seven coordinate cases including screen clamping and
original numeric-prefix behavior, PointerRoot focus, and three invalid inputs
without pointer/focus mutation. Each invocation allocates and tears down its
own Xvfb display; it never changes an existing user display or uses Internet
access. Dependencies are ordinary official target providers: gcc/glibc-devel,
make, tar/gzip/coreutils, libX11-devel, Python 3 and Xvfb. The tests subpackage
requires the matching program, Python 3, libX11 and Xvfb.

Full official and supplemental primary/filelists were screened for providers,
canonical aliases, RPM names and projected paths; the unpublished Liblcf-only
main delta has no overlap with this X11 utility. Metadata admission is not a
target solver or physical-product acceptance. The locked openEuler 24.03 SP3
riscv64/RVA23 target build, installation, complete CI and RPM/SRPM verification
must pass before explicit protected squash. No local RPM/QEMU build, native
input/hardware, timing, security, performance or exhaustive X11 conformance
claim is made. Auto-merge stays disabled.
