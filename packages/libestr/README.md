# libestr

This directory packages libestr 0.1.11 for openEuler 24.03 LTS SP3 on
`riscv64`/RVA23.

The frozen discovery snapshot cross-checks the canonical component across
Debian stable, Fedora 44, openSUSE Tumbleweed, and Ubuntu 26.04 LTS. No
distribution packaging content was executed.

The original project download host was independently checked but was not used
as an unverifiable fallback when it timed out. The pinned bytes instead come
from the official rsyslog/libestr repository's exact `v0.1.11` tag. The
archive SHA-256 is recorded in `sources.yaml`; it has one
`libestr-0.1.11/` root, no unsafe paths, and LGPL-2.1-or-later terms in
`COPYING` and source headers.

The official tag archive requires the standard upstream Autotools bootstrap.
The RPM retains upstream `make check` and adds a compiled public-API check
because upstream ships no standalone regression cases. Installed smoke tests
create a string and verify the library version entirely offline.
