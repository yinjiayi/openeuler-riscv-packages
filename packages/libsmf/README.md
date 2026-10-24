# libsmf 1.3

This package reads and writes Standard MIDI Files and retains the default shared
and static libraries, C header/pkg-config interface, manual and Readline-linked
interactive `smfsh`. It is deterministic userspace file/tempo arithmetic, not
MIDI hardware playback, wall-clock timing or a performance claim.

## Fixed source and discovery

The official SourceForge libsmf release feed still publishes 1.3 (2010-03-21)
and `libsmf-1.3.tar.gz`. The fixed official HTTPS archive has SHA-256
`d3549f15de94ac8905ad365639ac6a2689cb1b51fdfa02d77fa6640001b18099`
(545850 bytes); its published MD5 also matches but is not a strong authenticity
proof. No detached signature was captured. The feed's migrated GitHub URL
currently returns 404: this is not a claim that an unavailable repository has
no newer release. Discovery lineage is the frozen Arch extra, Debian stable/main
and Ubuntu resolute/universe catalog; no distribution packaging code is reused.

## Rights and complete original notices

The official project explicitly describes BSD-licensed software; COPYING and
core files retain their full BSD-2-Clause grants, including the original unusual
disclaimer. The short VLQ routine attribution in smf_save.c is retained under
that file's BSD grant, with no contrary separate grant found in the archive.
All 36 original archive files are preserved as inert .notice copies before
normal configure helper refresh; their original path structure and SHA-256
manifest remain installed. No original source or notice is edited.

GNU helper notices include GPL-2.0-or-later with Autoconf or Libtool exceptions,
FSFAP copying grants, FSFUL unlimited-copy notices, and the full X11 install-sh
grant including its advertising-name restriction (FSF changes there are public
domain). Complete GPL2/GPL3 texts are independently pinned at an immutable
official GCC mirror commit. The added API driver is ISC and ships its grant.

Default smfsh links target Readline 8.2 under GPLv3-or-later. The original
BSD-2-Clause grant is GPL-compatible; distribution of the combined program must
honor GPL3-compatible terms and corresponding-source obligations for the
program and linked dependencies. Nothing here relicenses the BSD library or
waives release-time source availability. The composite RPM expression
conservatively retains both linked-program obligations and original helper
notices, with 38 checksummed notice/text entries (39 files including manifest).

## Defaults and regression boundaries

Plain original configure retains its default Readline=check probe and default
shared/static builds. BuildRequires supply Readline/ncurses/GLib, and check
requires HAVE_LIBREADLINE plus an actual NEEDED libreadline entry, rejecting
silent feature fallback. Original make check remains unchanged: the supplied
Makefile.in check-am targets depend only on all-am and define zero upstream
runtime cases. No tests are removed, patched or skipped.

Six additional strict C API cases check version/defaults, exact independent
MIDI wire bytes (including VLQ480), memory/file decode+seek, tempo-map arithmetic
and persistence, format-one multitrack persistence, and invalid/text metadata.
Assertions are explicitly enabled for this driver. Check and installed smoke
replay the same driver with fresh temporary files. The installed driver and C
source have a post-strip SHA-256 manifest; raw loader trace/hash and real failed
exit status are retained. Six exact normal-symbol bindings must originate from
the absolute installed driver and resolve to the same physical installed
libsmf.so.0.0.0 using -ef, accepting legitimate /lib64/lp64d aliases without
loosening library identity. Version and interactive version-command output
are also asserted, not merely shell exit status.

The static official-base projection covers 18503 package records, 2207942
file records, 121 transitive provider packages and 60 version constraints,
including every declared command/header/library and proposed owned namespace.
It is not a DNF SAT solution or full supplemental namespace acceptance.

Only trusted recipe tooling and source verification run locally: no upstream C
compilation/execution, RPM build, QEMU or target QA is claimed. The recipe
requires no undeclared network fetch; actual target CI bridge is network-enabled
and checks pinned inputs, so this is not a network-isolation claim. Target
riscv64/RVA23 build, install and physical RPM/SRPM acceptance remain pending.
