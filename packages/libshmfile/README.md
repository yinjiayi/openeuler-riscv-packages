<!-- SPDX-License-Identifier: Apache-2.0 -->
# libshmfile

Official kata198/shmfile stable 1.1.0 is pinned to commit
`800c3d1bac0dd899c3d8737116db59334a828f31`, tree
`142f0ff1abaa7f7e7c2e06224de51506592e8123`. All twelve original archive
files match their authenticated Git blobs; archive SHA-256 is
`8b53b97b925a2884eda66b266943dc0b2130683b5fb4b5ec6a9a29dd417954a1`.
Discovery/AUR is lineage only, not a recipe or release authority.

All source notices specify LGPL version 2.1, without an “or later” grant:
the RPM therefore uses LGPL-2.1-only. Original complete LICENSE, copyright
notices and example headers remain unchanged. The complete official GPL2
companion is separately pinned in sources.yaml and installed as a license
record. No signature is supplied; HTTPS/Git identity/SHA-256 are not a
signature-verification claim. Original packaging/fixtures are Apache-2.0;
that does not relicense upstream code.

The default Makefile `all` target builds the original shared library and
manual; original `static` and `examples` targets are also built. There is
no registered upstream test/check target. No source patch, warning removal,
feature disable or source-tree rewrite is introduced. Upstream hardcodes
`lib` beneath PREFIX; installation relocates its two library files to
openEuler lib64, preserving their original unversioned names. The runtime
owns libshmfile.so; devel owns the original static library and header.
No invented stable SONAME/ABI promise is made.

Package CI 38960538174 built the unchanged original targets and passed both
staged shared/static functional replays, then failed with an empty RPM
debuginfo file list. The recipe had normalized the ELF library to mode 0644
before `find-debuginfo`; keep its executable bit at 0755 and normalize only
the public header to 0644. Default debuginfo/debugsource packaging, debug
flags and all tests remain enabled. This is a packaging permission fix,
not an upstream or RISC-V source patch; replacement-head CI and actual
debug RPM inspection must establish its result.

A **functional stream replay** here means sequential FILE/file-descriptor
operations using the packaged riscv64 library; it does not establish native
interprocess timing, concurrent access, permission isolation, memory safety,
resource-leak freedom, security or performance. This scope uses ordinary
QEMU user-mode file I/O; native/kernel/privileged claims remain unvalidated.

The unchanged original owner/guest sources and private example header are
SHA-256-bound and shipped for installed-header replays. Both shared and
static consumers run the original owner with its explicit zero-second
argument and persistent mode, followed by two original guests checking
the message and access counter, explicit destruction, missing-object and
invalid-argument negative controls. No sleep race or polling replaces an
original test. An additional clearly downstream fixture checks version,
buffered write/read/seek, descriptors and automatic unlink; it is not an
upstream test suite. Every failure propagates. Names are unique per run,
only owned objects are cleaned, and failed scratch directories are retained.
The staged `%check` route and installed smoke route must both pass; smoke
first runs `rpm -V` on installed runtime/devel files.

Fresh complete official 18,503 and supplemental 1,266 package primary and
filelists metadata found no RPM/capability/header/library/man/test-path
collision; audited build dependencies have metadata closure. That is not
a DNF solver or build-success claim. Exact-head hosted immutable-image
dependency resolution, original build, complete staged/installed replays
and physical RPM/SRPM acceptance remain mandatory. No local source/target
execution, RPM/QEMU build, Auto-merge, merge or public release is claimed.
