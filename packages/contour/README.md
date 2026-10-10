<!-- SPDX-License-Identifier: Apache-2.0 -->
# contour

This directory packages upstream `https://github.com/contour-terminal/contour` version `0.6.3.8249` for openEuler 24.03 LTS SP3 on `riscv64`/RVA23.

Release 6 declares the complete XKB and Qt 6 Wayland development closure exercised by the upstream Linux GUI build and gives the QEMU build a 120-minute package budget. The upstream unit-test targets remain enabled through `CONTOUR_TESTING`, and `%check` runs the generated CTest suite.

Release 7 increases only the package budget to 240 minutes after exact-head
evidence showed that dependency preparation left 4,852 seconds for an
error-free build that was still progressing at 65%. GUI, Wayland, and the full
CTest suite remain enabled without source changes.

External source and patch licenses remain those of their respective upstream projects. The repository license only covers original packaging metadata, scripts, and documentation.

Release 8 links `ContourTerminalDisplay` to the already selected yaml-cpp
target. Run `34232036793` compiled the bundled yaml-cpp provider, but the
display target did not inherit its include path and failed on
`yaml-cpp/emitter.h` through `Config.h`. The patch supports both namespaced
and legacy yaml-cpp targets and leaves GUI, Wayland, CTest, and the
240-minute budget unchanged; it does not add a second provider.
