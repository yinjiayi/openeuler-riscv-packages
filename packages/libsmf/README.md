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

The updater scans the complete RSS XML, so its selector matches the exact
archive basename at path/XML boundaries instead of anchoring to the complete
document. It rejects documentation, prerelease and extra-suffix lookalikes;
the official feed and canonical source URL template are unchanged. Regression
checks use retained official RSS bytes, not a fresh-release availability claim.

## Rights and complete original notices

The official project explicitly describes BSD-licensed software; COPYING and
core files retain their full BSD-2-Clause grants, including the original unusual
disclaimer. The short VLQ routine attribution in smf_save.c is retained under
that file's BSD grant, with no contrary separate grant found in the archive.
All 36 original archive files are preserved as inert .notice copies before
normal configure helper refresh; their original path structure and SHA-256
manifest remain installed. Original notice bytes are copied before the downstream
source patch; none of these original notices is edited.

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

## Downstream buffer-lifetime repair

The original smf_extend evaluates old base/track pointers after successful
realloc, outside their allocation lifetime. The package patch saves integer
offsets while the original allocation is live and reconstructs from only the
returned new base. Failed offset allocation/realloc retains the original owned
buffer and length; invalid/overflowing extension sizes fail before allocation.
NULL inactive tracks stay NULL. Loading's borrowed external input is not adopted:
the original successful loader clears all file-buffer fields before returning.
No crash, corruption, exploit, native-only defect or failing historical CI is
claimed. The fix is downstream-only; remove it when official stable source
provides equivalent lifetime-safe reconstruction and ownership handling.

Target-only additional controls preserve default make check (zero upstream
runtime cases), all six build/installed APIs and all six installed bindings.
A forced-moving allocator tests repeated offsets, NULL tracks and allocation
failure ownership, then two exact four-track wire/load/save roundtrips. It
includes the complete patched writer source with private symbol renaming; the
unchanged API cases separately exercise the actually linked patched library.
Moving allocations do not imply that the original undefined arithmetic must
fail at runtime. A distinct GCC-specific negative compiles exact preserved
original source with -Wuse-after-free=3 -Werror=use-after-free and requires compiler exit1/make2,
the original line77 previous_file_buffer error and line65 realloc note, no
unrelated error/fatal-error diagnostics, and no object. Multiple identical
causal diagnostics are permitted, not claimed unique. The patched source must
first compile with the same flags. Unsupported/wrong diagnostics fail closed.
Full raw compiler streams/status and hashes are emitted. These controls are
mandatory target CI checks, not locally executed proof or general parser safety.
The added regression source retains its full ISC grant in the SPEC/SRPM.
