# most

This package tracks the official Most 5.2.0 release for openEuler 24.03 LTS
SP3, riscv64 RVA23. Source0 is fetched over HTTPS and pinned by SHA-256.
The build uses the target distribution's `slang-devel` package.

Upstream provides manual test files but no automated `check` target. The RPM
`%check` exercises non-interactive stdin and file paging with the newly built
binary. The installed-package smoke test repeats stdin paging and reads an
installed documentation file. Neither test proves interactive terminal behavior;
target CI provides RISC-V build and installation evidence.
