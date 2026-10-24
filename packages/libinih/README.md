# libinih

This package tracks the official inih r62 tag for openEuler 24.03 LTS SP3,
riscv64 RVA23. Source0 is downloaded over HTTPS and pinned by SHA-256.

The Meson build preserves both C and C++ libraries. `%meson_test` runs the
upstream 15-configuration C parser matrix and C++ INIReader example. The
installed-package smoke test loads both shared libraries, parses a small INI
string through the C API, and checks development headers. Target CI establishes
the RISC-V build and installed result; no local RPM/QEMU build is claimed.
