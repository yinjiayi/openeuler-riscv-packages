<!-- SPDX-License-Identifier: Apache-2.0 -->
# gtk4-layer-shell

This directory packages upstream `https://github.com/wmww/gtk4-layer-shell` version `1.3.0` for openEuler 24.03 LTS SP3 on `riscv64`/RVA23.

Release 3 retains the GTK4, Wayland, GObject introspection, Vala, Python, and
PyGObject dependencies supplied by the fixed openEuler target repository. It
enables all 40 layer-shell integration tests, 11 session-lock integration
tests, one unit test, and six smoke tests. The three example binaries used only
by smoke tests are built explicitly while Meson's `examples` installation
option remains disabled, so the test contract is preserved without adding the
demo application to the RPM payload. A downstream test-harness patch keeps the
upstream timeout multiplier default of one and lets the qemu-user `%check`
phase multiply internal display, client, server, and smoke-example deadlines by
ten; all 59 tests and Meson's existing parallelism remain enabled.

Exact-head Package CI run `33547667881` compiled and installed Release 2, then
passed 53 of 59 tests. All six smoke tests exhausted fixed one-second internal
harness deadlines under qemu-user; no test was skipped, and no RPM, SRPM, or
publication result was produced. Release 3 requires a fresh exact-head target
run before its RISC-V status can be updated.

External source and patch licenses remain those of their respective upstream projects. The repository license only covers original packaging metadata, scripts, and documentation.
