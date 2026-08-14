<!-- SPDX-License-Identifier: Apache-2.0 -->
# psmisc

This directory packages psmisc 23.7 for openEuler 24.03 LTS SP3 on
riscv64/RVA23. Fedora 44, Arch stable, Debian stable, openSUSE Tumbleweed, and
Ubuntu all independently track the upstream 23.7 release. AUR was queried only
through its read-only RPC for psmisc-selinux metadata; no PKGBUILD, install
hook, patch, or command from AUR was read or executed.

The official generated SourceForge 23.7 release archive is pinned by SHA-256.
Archive inspection found one psmisc-23.7 root and no absolute path, parent
traversal, link, or special entry. The build enables SELinux support and uses
only BuildRequires already available in the openEuler 24.03 SP3 riscv64
repository. It updates the target's existing 23.6 package without introducing
a library ABI.

The SPEC runs the complete upstream `make check` gate, including the DejaGNU
killall, pslog, and fuser suites; none is skipped or marked non-fatal. The
installed smoke test verifies every architecture-independent process utility
and confirms that fuser discovers a live file descriptor. RISC-V status
remains unknown until the pinned openEuler RVA23/QEMU workflow completes.

External source licenses remain upstream's. Apache-2.0 covers only this
repository's original packaging metadata, scripts, tests, and documentation.
