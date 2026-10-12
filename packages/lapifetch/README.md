<!-- SPDX-License-Identifier: Apache-2.0 -->
# lapifetch

This directory packages upstream `https://github.com/asunyan-dev/lapifetch` version `1.4.0` for openEuler 24.03 LTS SP3 on `riscv64`/RVA23.

External source and patch licenses remain those of their respective upstream projects. The repository license only covers original packaging metadata, scripts, and documentation.

Packaging release 2 passes the RPM macro build directory explicitly to CMake so the configure, build, install, and test phases share the same out-of-tree build.

Packaging release 3 declares the X11 and RandR development providers and carries a minimal MIT patch matching upstream's Makefile and Nix link libraries.
