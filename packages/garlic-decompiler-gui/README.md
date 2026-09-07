<!-- SPDX-License-Identifier: Apache-2.0 -->
# garlic-decompiler-gui

This directory packages upstream `https://github.com/AgarwalKritik/garlic-gui` version `1.1.0` for openEuler 24.03 LTS SP3 on `riscv64`/RVA23.

Release 3 configures, builds, installs, and checks the project through the same
explicit out-of-source CMake directory. Upstream 1.1.0 does not register CTest
cases; the package retains CTest discovery and verifies that the complete build
produced the real `GarlicGUI` executable. The installed smoke test verifies the
RPM and installed executable without attempting to launch a GUI without a
display server.

External source and patch licenses remain those of their respective upstream projects. The repository license only covers original packaging metadata, scripts, and documentation.
