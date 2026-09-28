# libart-lgpl

This package targets openEuler 24.03 LTS SP3, riscv64 RVA23 with the GNOME
Libart 2.3.21 release. The HTTPS archive checksum matches GNOME's own
`sha256sum` index. The old AUR discovery row was marked stale; no AUR build
recipe was read or executed.

Upstream's `tests` target builds `testart` and `testuta` but does not run
them. The RPM `%check` executes every documented `testart` mode and `testuta`
and verifies they produce output. Installed smoke calls the library's affine
identity API and checks its version symbols. These are functional checks, not
pixel-perfect rendering validation; target CI must establish the RISC-V build
and installed result.
