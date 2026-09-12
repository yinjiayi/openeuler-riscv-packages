<!-- SPDX-License-Identifier: Apache-2.0 -->
# session-lock-qt

This directory packages upstream `https://github.com/waycrate/qt-session-lock` version `2.1.0` for openEuler 24.03 LTS SP3 on `riscv64`/RVA23.

Downstream release `4` matches the pinned archive's exact `qt-session-lock-2.1.0` source root, loads `Qt6::WaylandClientPrivate` through openEuler Qt 6.5's public `WaylandClient` component, and keeps the private target and all Wayland session-lock functionality enabled. Its compatibility patch retains the common `requestActivate()` path, keeps the newer `requestActivateOnShow()` method without requiring that Qt 6.5 already declare it as virtual, and corrects the Qt 6.5 expose-size member reference. It declares the matching Qt base private headers, Qt Wayland development files, XKB development provider, and Wayland protocol dependencies. The build uses one explicit out-of-source directory and verifies that the upstream `sessionlock-test` executable is produced. The source SHA-256 remains unchanged.

Release `5` corrects the header hunk's surrounding context in the existing
Qt 6.5 compatibility patch, without changing its source edits. GNU patch with
`--fuzz=0` rejected the previous asymmetric final hunk even though Apple patch
accepted it. The revised hunk uses two unchanged lines on each side and passes
GNU patch's zero-fuzz dry run against the pinned source archive. Target build
and session-lock behavior still require fresh CI and runtime evidence.

Release `6` adds the direct public `QGuiApplication` include used by
`requestActivate()`. After the patch-format repair, compilation reached that
method but Qt 6.5's private headers did not declare the application class
transitively. This only makes the existing dependency explicit; activation
behavior, the compositor test executable, and all build checks are retained.

External source and patch licenses remain those of their respective upstream projects. The repository license only covers original packaging metadata, scripts, and documentation.
