# librcnb 1.0.0

Official rcnbapp/librcnb v1.0.0 is pinned to commit
45dd2e77d3f06165c7f0511d9556b88b4497c0dc. The fixed archive SHA-256 is
f5d391114fbe0307b7cbc43ebc94e25472e867af3c318dbd60e7c22b9790d38e;
all 21 original archive files agree with their Git blobs. Root MIT and literal
public-domain notices are preserved, without relabeling those notices Unlicense.
Historical AUR lineage is discovery evidence only; no PKGBUILD was executed.

All original default CMake targets remain: shared and static libraries, three
C/C++ examples and the rcnb CLI. Release optimization remains, with assertions
enabled. The original AppVeyor CLI round-trip vector is run byte-for-byte;
there is no upstream CTest suite, and an empty test target is not success evidence.
The original Python shared-library example and asserted C example are retained.
The other original examples are built and shipped unchanged, not claimed as
separately validated functional tests.

The sole downstream patch repairs a portable decoder boundary defect: four
complete encoded wchar_t values must be consumed even when no further input
remains. This is an inert source/state-trace finding, not a locally reproduced
RISC-V failure. 706 downstream shared-library regression checks cover all
single bytes, 32 lengths, chunk widths 1–13, empty and invalid input. These are
not upstream case counts or proof of target success before CI.

Source/staged/installed phases must pass using the corresponding actual library.
Installed smoke checks RPM integrity/ownership and canonical loader-path
equivalence; it never falls back to a source tree or another library. Genuine
RPM/SRPM, source checksums, exact-head full CI and current-main evidence remain
required before merge or publication. No local RPM/QEMU/upstream run is allowed.
