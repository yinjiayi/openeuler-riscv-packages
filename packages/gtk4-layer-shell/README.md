<!-- SPDX-License-Identifier: Apache-2.0 -->
# gtk4-layer-shell

This directory packages upstream `https://github.com/wmww/gtk4-layer-shell` version `1.3.0` for openEuler 24.03 LTS SP3 on `riscv64`/RVA23.

Release 5 retains the GTK4, Wayland, GObject introspection, Vala, Python, and
PyGObject dependencies supplied by the fixed openEuler target repository. It
enables all 40 layer-shell integration tests, 11 session-lock integration
tests, one unit test, and six smoke tests. The three example binaries used only
by smoke tests are built explicitly while Meson's `examples` installation
option remains disabled, so the test contract is preserved without adding the
demo application to the RPM payload. An internal deadline is a timeout enforced
inside the Python integration harness around display, client, server, or smoke
operations. The Meson external watchdog is the separate per-test limit that can
terminate the whole harness. A downstream patch keeps the internal multiplier
default at one, while the qemu-user `%check` phase sets both multipliers to ten.
The package budget is raised from 60 to a bounded 90 minutes so Meson's resulting
1200-second limit can finish before the enclosing CI deadline; all 59 tests and
Meson's existing parallelism remain enabled.

Exact-head Package CI run `33660703308` compiled and installed Release 4, then
passed 58 of 59 tests. `lock-test-multiple-monitors` exceeded Meson's unchanged
120-second outer limit even though the qemu-user internal deadlines had already
been scaled; no test was skipped, and no RPM, SRPM, or publication result was
produced. Release 5 requires a fresh exact-head target run before its RISC-V
status can be updated.

External source and patch licenses remain those of their respective upstream projects. The repository license only covers original packaging metadata, scripts, and documentation.
