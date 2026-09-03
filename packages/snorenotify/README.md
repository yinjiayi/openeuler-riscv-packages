<!-- SPDX-License-Identifier: Apache-2.0 -->
# snorenotify

This directory packages upstream `https://github.com/KDE/snorenotify` version `0.7.0` release `3` for openEuler 24.03 LTS SP3 on `riscv64`/RVA23.

The upstream CMake configuration requires Extra CMake Modules and the Qt5 Core, Network, and Gui components, while Qt5 Widgets, D-Bus, and Test support enable the desktop notification paths and unit tests. Release `2` declares `extra-cmake-modules` and `qt5-qtbase-devel` so these existing features and tests remain available during the RPM build. Release `3` extends the audited build timeout because that required Qt5 dependency closure did not finish downloading within 60 minutes from the fixed target repositories; no dependency or source was changed.

External source and patch licenses remain those of their respective upstream projects. The repository license only covers original packaging metadata, scripts, and documentation.
