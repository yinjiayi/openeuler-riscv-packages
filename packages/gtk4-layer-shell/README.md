<!-- SPDX-License-Identifier: Apache-2.0 -->
# gtk4-layer-shell

This directory packages upstream `https://github.com/wmww/gtk4-layer-shell` version `1.3.0` for openEuler 24.03 LTS SP3 on `riscv64`/RVA23.

Release 2 declares the GTK4, Wayland, GObject introspection, Vala, Python, and
PyGObject dependencies supplied by the fixed openEuler target repository. It
enables all 40 layer-shell integration tests, 11 session-lock integration
tests, one unit test, and six smoke tests. The three example binaries used only
by smoke tests are built explicitly while Meson's `examples` installation
option remains disabled, so the test contract is preserved without adding the
demo application to the RPM payload.

The prior exact-head Package CI run was cancelled before package analysis and
produced no build artifacts. Consequently, the RISC-V status remains unknown
until this release completes the protected exact-head target workflow; no RPM,
SRPM, or publication result is claimed here.

External source and patch licenses remain those of their respective upstream projects. The repository license only covers original packaging metadata, scripts, and documentation.
