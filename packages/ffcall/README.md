<!-- SPDX-License-Identifier: Apache-2.0 -->
# ffcall

This directory packages GNU libffcall 2.5 as the `ffcall` RPM for openEuler
24.03 LTS SP3 on `riscv64`/RVA23. GNU's official archive index lists 2.5 as
the highest stable release. The exact archive is pinned by SHA-256
`7f422096b40498b1389093955825f141bb67ed6014249d884009463dc7846879`.

The archive contains 674 members below one `libffcall-2.5` root. It has no
absolute or parent-traversal paths, symbolic or hard links, or special files.
Upstream's `COPYING`, README, bundled gnulib notices, and manual headers cover
GPL-2.0-or-later, LGPL-2.1-or-later, and dual GPL/GFDL-1.2-or-later content.
GNU's release index does not provide a detached signature for this archive;
the pinned full SHA-256 is the required source contract.

Frozen snapshot `discovery-20260808T165000Z-9a89920c269462cd` records Arch
extra `2.5-1`, Debian stable `2.5-2`, Fedora 44 GA `2.5-6.fc44`, openSUSE
Tumbleweed `2.5-1.7`, and Ubuntu 26.04 LTS `2.5-2`. Its stale AUR row is kept
as metadata-only corroboration; no AUR or distribution recipe was executed.

Neither the fixed openEuler repository nor supplemental generation
`wdiff-44fa7d2c053dca8215e98f866d0f74ce7b0d3d5d-31617819790-1` provides
ffcall, libffcall, or any of its shared-library SONAMEs. The package therefore
owns the libffcall, avcall, callback, and trampoline shared runtimes.
Development links, public headers, and manuals are in `ffcall-devel`; all five
static archives are isolated in `ffcall-static`.

The complete upstream C and C++ test matrix runs in `%check`; no test target
or feature is disabled. Upstream's RISC-V assembly templates contain PIC and
non-PIC branches. The build selects the PIC branch for static `libvacall.a`,
and the test objects and executables retain openEuler's PIE hardening. The
installed smoke compiles and executes a real `avcall` invocation on the target
architecture and checks all shared-library SONAMEs. Build dependencies may be
acquired online before `rpmbuild`; source verification and the RPM build itself
remain offline and digest-bound.

External source licenses remain those of upstream. Apache-2.0 covers only the
original packaging metadata, test, and documentation in this directory.
