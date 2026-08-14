<!-- SPDX-License-Identifier: Apache-2.0 -->
# xmlstarlet

This directory updates XMLStarlet `1.6.1` for openEuler 24.03 LTS SP3 on
`riscv64`/RVA23 from target release 14 to release 15. SourceForge's official,
immutable 1.6.1 release archive is pinned by SHA-256. It is single-rooted; all
paths and hard links resolve inside that root, and it contains no unsafe links
or special members. The archive includes the upstream MIT license and the
complete maintained examples test suite.

Arch stable, Debian, Fedora 44 GA, openSUSE Tumbleweed, Ubuntu, and the fixed
target all corroborate version 1.6.1. Read-only AUR RPC metadata was considered;
no AUR PKGBUILD or distribution recipe was read or executed. Release 15
preserves the target package name, executable, help split, EVR ordering, and
existing libxml2/libxslt ABI requirements.

`%check` runs all 79 upstream examples. A fresh native RISC-V compatibility
run against openEuler 24.03 SP2's libxml2 2.11.9 and libxslt 1.1.39—the same
upstream library versions as SP3—reported 77 PASS, two canonical XFAIL, and
zero FAIL or ERROR. This does not replace the SP3/RVA23 QEMU package CI.
Installed smoke transforms and selects XML using the public command interface.

External source licenses remain those of upstream. Apache-2.0 covers only the
original packaging metadata, scripts, tests, and documentation here.
