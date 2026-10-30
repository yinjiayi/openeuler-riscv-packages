# Hedley 15

The official `nemequ/hedley` stable `v15` tag resolves to
`8fb0604a8095f6c907378cc3f0391520ae843f6f`. Its archive SHA-256 is
`aea6cb90997d67b4706166a761207c6bb833e201937c46ee8dd170b6e8cc6730`.
All51 original files/modes match that Git tree. The complete COPYING is
CC0-1.0 and is shipped in both binary packages. No source patch is applied.

`hedley` installs the public header. `hedley-tests` installs the original
Makefile and all36 C test inputs;35 of them belong to upstream's default
`all` target. That target compiles and links35 C plus35 C++ programs, and
also generates the original auxiliary Makefiles. These70 programs are
compiler conformance targets, not runtime test cases. Some deliberately
demonstrate runtime-unsafe code and must not be executed as a runtime suite.
The original GCC/G++ warning flags and three per-target diagnostic exceptions
are preserved unchanged. Neither C++ nor any default target is disabled.

The original G++ diagnostic rules for `unknown-pragmas`, `unavailable` and
`warn` deliberately use the same output filenames as their C counterparts.
Thus all70 compiler commands produce67 final executable files, not70 files.
QA checks every expected filename and the exact67-file count without changing
those upstream rules. The programs are never executed as runtime tests.

`%check` runs the complete default target and repeats it in a fresh tree
using the staged installed header and QA sources. Installed smoke verifies
both RPMs and repeats all70 compile/link targets against the actual installed
header. No ELF program is shipped, so debug RPM splitting is inapplicable.
The target remains openEuler24.03 LTS SP3/riscv64/RVA23 with pinned CI image;
local checks do not establish target build/install success.

Debian SIMDe0.8.2-1's vendored Hedley header is component-discovery evidence.
Its vendored version16 is not claimed identical to proposed stable15, and
SIMDe is not presented as a standalone Debian Hedley package. Compatibility
and namespace screening use full target provider metadata, independently
of this discovery lineage.
