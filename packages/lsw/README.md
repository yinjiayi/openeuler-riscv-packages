# Lsw 0.3

List X11 window titles and XIDs. Canonical discovery component:
`tools.suckless.org-x-lsw`, snapshot
`discovery-20260808T165000Z-9a89920c269462cd` (Arch/Fedora lineage).

Official release: https://tools.suckless.org/x/lsw/ and fixed archive
https://dl.suckless.org/tools/lsw-0.3.tar.gz. SHA-256:
`0b3f3ce16eef060df6e0d90327ee82593dfd75281347908698747cfa3f8d0655`.
All six members, including the MIT/X Consortium notice, were read. No release
signature is advertised; none is claimed. Source archives stay out of Git.

The unmodified upstream default `all` builds the Xlib utility. Upstream has no
check/test target; no original suite is removed or fabricated. Packaging adjusts
compiler/hardening flags and standard distro include/library/install paths only,
keeps all functionality, and permits RPM's normal separate debug output.
There are no source patches. The tests subpackage retains the whole official
archive and downstream QA embedded in the SPEC, hence also in the SRPM.

Build dependencies: GCC, glibc-devel, make, tar, gzip, coreutils, sed, libX11-devel,
Python 3 and xorg-x11-server-Xvfb. Runtime Xlib is automatically generated from
ELF dependencies; the tests subpackage adds Python/Xvfb. Both providers are present
in the fixed official RVA23 target metadata. All current main/open PR package
names and paths are screened before submission; admission screening is not
physical RPM acceptance or a DNF solver.

The same staged and installed downstream checker allocates an unused Xvfb display
with `-displayfd`, disables TCP, and uses Xlib to create controlled windows. It
asserts root and explicit-parent selection, nested windows, hidden and
override-redirect filtering, modern-title precedence, fallback names, visibility
transitions and a deterministic missing-display error. All processes are bounded
and cleaned up. There is no external test network, skipped test, ignored failure,
local source execution, local RPM build or local QEMU run.

QEMU-user hosted CI must still prove source/build, normal all-binary installation,
installed QA, and exact-head RPM/SRPM payload, dependency and namespace acceptance.
These offline X11 functional checks do not validate native graphics hardware,
desktop integration, timing, performance or security. Auto-merge is not enabled.
