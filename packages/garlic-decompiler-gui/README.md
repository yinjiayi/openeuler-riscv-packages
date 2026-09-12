<!-- SPDX-License-Identifier: Apache-2.0 -->
# garlic-decompiler-gui

This directory packages upstream `https://github.com/AgarwalKritik/garlic-gui` version `1.1.0` for openEuler 24.03 LTS SP3 on `riscv64`/RVA23.

Release 3 configures, builds, installs, and checks the project through the same
explicit out-of-source CMake directory. Upstream 1.1.0 does not register CTest
cases; the package retains CTest discovery and verifies that the complete build
produced the real `GarlicGUI` executable. The installed smoke test verifies the
RPM and installed executable without attempting to launch a GUI without a
display server.

Release 4 removes upstream's blanket `-Wno-format` suppression for the embedded
C core. This keeps openEuler's `-Wformat-security` check active and avoids the
GCC 14 error caused by combining a disabled prerequisite warning with
`-Werror=format-security`.

External source and patch licenses remain those of their respective upstream projects. The repository license only covers original packaging metadata, scripts, and documentation.

Release 5 supplies balanced context in the existing format-security patch.
GNU patch rejected the asymmetric hunk with RPM's
zero-fuzz policy even though macOS BSD patch accepted it. The change preserves
the original single-line deletion and all compiler diagnostics and checks.
