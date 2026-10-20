<!-- SPDX-License-Identifier: Apache-2.0 -->
# lr

Official stable v2.0.1 is fixed to commit bfb868dae062fdd5a1fac3d33eca7821cd751d10
and the original archive SHA-256. Current non-VCS AUR lr2.0.1-1 corroborates
discovery; no frozen catalog membership or stale lr-git authority is claimed.
All 12 original members are preserved and reviewed (11 text files, one sample
screenshot). LICENSE and the complete lr.c notice retain their different Leah
copyright years and the original Rich Felker/musl attribution in both packages.

Original all/install, compiler warnings and default zsh completion are retained.
Only standard RPM paths/flags and a small source-input-boundary patch are used.
The patch checks decimal/suffix arithmetic and relative times, rejects too-long
prefixes before array access, terminates three-marker xattr storage, and rejects
incomplete format escapes. It does not remove recursion/filter/order/format or
other default features. No original test/check target exists; none is skipped.

Mandatory target regression builds SHA-bound original and patched source with
instrumented ordering/bounds controls before unsafe operations, including
negative original controls and ordinary valid cases for both. Poisoned allocated
storage and logical-end sentinels are deterministic models, not allocator,
ASan/UBSan, native hardware or general memory-safety proof. Assertions cannot be
disabled by inherited NDEBUG. No local source/compiler/target execution occurred.

Mandatory bounded offline functional QA runs the actual built, staged and
installed default executable with private HOME and temporary files. It checks
default recursion/order, hidden/prune/depth, types/size/time expressions, input
lists/NUL, symlinks, formatting/quoting, traversal orders, colors/NO_COLOR,
hyperlinks and strict CLI/input errors. Completion syntax and original byte-exact
manual/license/readme/completion checks remain mandatory after installation.
No native/performance/all-filesystem/xattr-kernel coverage is claimed. Complete
exact-head hosted CI, ordinary DNF installation, physical RPM/SRPM ownership and
publication remain separate acceptance gates.
