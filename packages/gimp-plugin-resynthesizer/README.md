<!-- SPDX-License-Identifier: Apache-2.0 -->
# gimp-plugin-resynthesizer

This directory packages upstream `https://github.com/bootchk/resynthesizer` version `3.0.1` for openEuler 24.03 LTS SP3 on `riscv64`/RVA23.

The upstream Meson build requires the `pkgconfig(gimp-3.0)` and `pkgconfig(glib-2.0)` development interfaces, supplied by `gimp-devel` and `glib2-devel` on the target repository.

Release 3 raises the package timeout from 60 to 180 minutes. Exact-head run
`33362605060` resolved a 328-package dependency transaction but exhausted the
former budget while downloading package 114, before `rpmbuild` began.

Exact-head run `33719340367` completed the same dependency transaction and then
failed deterministically in `%prep`: the verified GitHub tag archive expands to
`resynthesizer-3.0.1`, not a directory derived from the downstream RPM package
name. Release 4 selects that verified directory explicitly. Upstream does not
register a Meson `test()` target, so the build enables and executes its
`testHealLib` functional harness directly and requires all eight scenarios to
run. The RISC-V build status remains `unknown` pending fresh exact-head build and
installed-smoke evidence.

Exact-head run `33721116347` confirmed the source-directory fix, then failed
while compiling the optional `libheal` target because its `imageSynth.c`
translation unit used the `Pixelel` and `Coordinates` types without including
their defining headers. Release 5 adds those two direct dependencies in the
same order already used by upstream `engine.c`; no algorithm or plugin behavior
is changed. The eight-scenario `testHealLib` execution and count gates remain
mandatory.

Exact-head run `33722153814` compiled all 34 targets, including the repaired
`libheal`, then failed in `%install` because upstream v3.0.1's custom i18n copy
commands used absolute `/usr` paths and ignored RPM's `DESTDIR`. Release 6
prefixes the generated catalog source and every bundled per-plugin translation
destination with `DESTDIR`. This is the minimal stable-release equivalent of
upstream commit `f38a155f9168a29460380642b4f1cbcc81a5186b`, which later replaced
the loop with a `MESON_INSTALL_DESTDIR_PREFIX`-aware installer. The RISC-V build
status remains `unknown` pending fresh exact-head build and installed-smoke
evidence.

Exact-head run `33723518309` confirmed that every custom translation copy now
stays inside the RPM buildroot, then failed at the non-empty `%check` guard
because upstream only enters `test/` when its separate `install-test` option is
enabled. Merely enabling `build-libheal` therefore built the repaired library
but not `testHealLib`. Release 7 enables those upstream CI/developer targets so
the functional harness is materialized, then removes the installed harness and
developer-only GIMP test plugin before generating the runtime file list.
`%check` executes the build-tree harness and still requires all eight scenario
markers.

Exact-head run `33724934486` then materialized `testHealLib` and exposed the
next upstream build-system defect at its link step: `libheal_sources` omitted
the existing map, coordinate, target-pixel, target-ordering, bounds, and
statistics implementation units used by `imageSynth.c` and `engine.c`.
Release 8 adds those same six support sources already compiled into upstream's
full `libresynthesizer` library. The harness remains a real linked executable
and its eight-scenario runtime gate is unchanged.

External source and patch licenses remain those of their respective upstream projects. The repository license only covers original packaging metadata, scripts, and documentation.
