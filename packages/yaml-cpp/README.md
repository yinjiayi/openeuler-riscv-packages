# yaml-cpp

This directory packages yaml-cpp 0.9.0 for openEuler 24.03 LTS SP3 on
`riscv64`/RVA23.

The frozen discovery snapshot cross-checks the canonical component across
Arch stable Extra, AUR metadata-only derivatives, Debian stable, Fedora 44,
and openSUSE Tumbleweed. No distribution or AUR recipe was executed.

The source is the immutable release asset published by the official GitHub
project. Its independently downloaded SHA-256 exactly matches the digest
published by GitHub for that asset. The asset intentionally expands as a flat
source tree, contains no absolute or parent paths, and carries the MIT license
in `LICENSE`.

The RPM builds the shared C++ library with the bundled upstream GoogleTest
suite enabled and runs all CTest tests. An installed smoke program parses and
emits a fixed YAML value through the public API. Build and tests are offline.
