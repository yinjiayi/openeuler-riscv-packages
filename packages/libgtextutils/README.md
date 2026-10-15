<!-- SPDX-License-Identifier: Apache-2.0 -->
# libgtextutils 0.7

Official tag `0.7`, commit `1f03f41e7c4740164aae44570fa8d05c3f3e7ed6`,
44 Git-blob-verified files, archive SHA-256
`e00f2fad261230f200507514e84b721024f8a88c35706572a86f5f1751f1ff3a`.
No detached upstream signature is provided. Frozen Debian stable lineage
`libgtextutils 0.7-9` in discovery-20260808T165000Z-9a89920c269462cd is a
discovery clue, not source or executable packaging. The older AUR row is stale;
it is not the admission basis. Official fixed source was freshly reverified.

The library is AGPL-3.0-or-later; Martin Pool's strnatcmp carries Zlib terms.
`LicenseRef-Josuttis-1999` means the inbuf1.hpp/outbuf3.hpp book-example
permission to copy/use/modify/sell/distribute while retaining the notice.
These original notices and the full AGPL are installed as license files.

Patch0001 is upstream-generic C++ compatibility, not a RISC-V-specific fix:
explicit stream-to-bool conversion preserves !fail() semantics; comparator
typedefs replace deprecated binary_function inheritance without changing
comparison bodies or type aliases. The original pipe test's intended empty
buffer is initialized before strcat; every assertion/case remains. No upstream
write was made. Remove when an official release supplies equivalent fixes.

Keep debug, strict wall/Werror, assertions and every original default feature.
`make check` runs all ten original default Automake programs, including gzip
pipes and file-descriptor streams. Two tuple parser programs retain their
original default-disabled configure condition, not a downstream suppression.
All original test sources are shipped; separate installed-library replay
compiles and executes the same ten default programs with strict diagnostics,
fresh per-program fixtures, SHA-256 checks and shared-link path verification
when a DT_NEEDED entry exists. No assertion count beyond ten programs is claimed.

Source-only verification and trusted repository tests do not establish target
build/install success. Target openEuler24.03LTSSP3/riscv64/RVA23 builds, original
tests and installed RPM checks run only in exact-head remote CI. No local
RPM/QEMU/upstream execution, Auto-merge or native validation claim.

External source and patch licenses remain those of their respective upstream projects. The repository license only covers original packaging metadata, scripts, and documentation.
