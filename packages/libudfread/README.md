# libudfread

VideoLAN's libudfread is a userspace reader for UDF filesystem images. This
package targets openEuler 24.03 LTS SP3, riscv64, RVA23. It does not mount an
image, access an optical drive, or claim native hardware/timing validation.

## Source and rights

The official VideoLAN release index lists the fixed 1.2.0 archive and its
SHA-512 file. The actual 28,732-byte archive has SHA-256
`bb477cbd4cfbfc7787d9d05b71ee5e70430f5cfebf1297497f7e83547958050f`;
the published SHA-512 also matches. The former developer HTML page returns
404; discovery lineage is retained, but it is not used as a working fetch URL.
No detached signature was captured and none is claimed.

All 26 safe regular source members are retained verbatim under
`license-notices/*.notice` before generating any package tests. C/header
members retain the LGPL-2.1-or-later grants and all original authors including
hpi1 and the VideoLAN authors. The five Meson files explicitly select MIT and
retain Rob Hall's 2025 copyright. Unmarked project configuration/history files
are preserved in full alongside the original project COPYING; there are no
bundled fonts, media fixtures, generated third-party code, or downloaded
subprojects. The original complete LGPL-2.1 text plus complete GPL2 and MIT
texts from a fixed SPDX license-list-data commit are installed. The generic
MIT legal text supplements, rather than replaces, actual per-file copyright
notices. A manifest checksums all 28 original/additional notice files both
in `%check` and after installation.

## Defaults and tests

The original Meson defaults remain: C99, debugoptimized/optimization 3,
shared **and** static libraries, the optional pthread probe, examples disabled,
and embed mode disabled. No default feature or test is removed. The unchanged
Meson test entry point is run, but upstream registers **zero** runtime test
cases. The examples are not default targets; this package does not claim that
the optional upstream CI examples constitute an original runtime suite.

Six additional assert-enabled API cases check version/invalid inputs, volume
identity, directories/missing files, a multi-block byte stream, seek bounds,
and block/relative reads. The expected 4,800-byte payload and nested file are
independently constructed; `genisoimage -udf` generates the regular-file image
inside actual target CI. The installed regression replays the same driver and
image, verifies their post-strip SHA-256 manifest, and checks six exact normal
symbol bindings from the installed absolute driver to the same physical file
as `/usr/lib64/libudfread.so.3.0.0` using `-ef`. It does not assume the loader
spells its path `/usr/lib64` instead of `/lib64/lp64d`. Raw loader traces and
their digest are printed on both success and driver failure; loader injection
variables are cleared before replay.

## Acceptance boundary

The complete checksum-bound official primary/filelists metadata supplies
Meson >=0.60, Ninja, the compiler/headers, genisoimage and all declared
transitive dependencies. Exact identities, aliases and proposed installed
paths have no official-base collision. This is a static provider projection,
not a claim about an unavailable fresh supplemental namespace or a complete
transaction solver.

Local checks run only trusted repository tooling, schema/source verification
and inert parsing. No upstream compilation/test, RPM, ELF, QEMU or target
execution takes place locally. Actual target build/install, physical RPM/SRPM,
notice preservation and supplemental evidence must still pass before merge.
The recipe performs no undeclared fetch; the actual trusted CI bridge remains
network-enabled and verifies pinned source bytes, so offline isolation is not
claimed.
