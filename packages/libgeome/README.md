<!-- SPDX-License-Identifier: Apache-2.0 -->
# libgeome

Official Libgeome 1.0, ISC (2025 Mattias Andrée), fixed Codeberg source archive.
SHA-256: `28f17577d0b264bec90cf0adb2ee23a51178a227138a6026f1b46cfd028a32a6`.
All 25 regular release files were reviewed; the unchanged archive and full ISC
notice are retained. Frozen discovery `discovery-20260808T165000Z-9a89920c269462cd`
contains the actual AUR lineage; no PKGBUILD execution or upstream write.

The default static/shared libraries and all five upstream driver programs are
built, without filtering. Upstream has no `make check` target. The installed
header and libraries retain SONAME `libgeome.so.1` and full version `1.0`;
the recipe relocates `/usr/lib/libgeome.*` to `/usr/lib64`. All optional network
services remain available. Runtime `curl` and `tzdata` are retained, not removed
to simplify a build. Applications must obtain consent for third-party requests.

One ISC downstream patch checks conversion consumption and ctype inputs,
bounds timezone coordinate fields before indexing, closes command pipes on all
paths, rejects oversized output rather than parsing a truncated prefix, and
reaps only the owned child with EINTR retry. These are portable source fixes,
not RISC-V-specific. No upstream submission. Remove after an equivalent fixed
official release passes these tests.

Staged and normally installed checks each compile all five unchanged original
drivers against static and shared installed libraries. Local time/timezone and
file/command fixtures are deterministic; a PATH-local `curl` executable supplies
known data to all seven original network-service entries. This validates the
original driver/API routing, not actual HTTP service availability or geolocation
accuracy. Independent consumers cover plain/CSV/JSON/XML values, empty and
invalid inputs, ranges, output limits and repeated command descriptor cleanup.
Malformed timezone fields are rejected. Assertions remain enabled.

Local validation is limited to repository metadata/tooling tests, shell syntax
and patch dry-run. No upstream source, RPM or QEMU executes locally. Exact-head
remote CI build/install/default-driver and physical RPM/SRPM acceptance remain
mandatory before explicit squash. These tests do not establish native signal,
kernel, concurrency, timing, security or location-accuracy guarantees.

Original packaging is Apache-2.0; upstream source and this patch remain ISC.
Every subpackage keeps the complete upstream license notice.
