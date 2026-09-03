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

External source and patch licenses remain those of their respective upstream projects. The repository license only covers original packaging metadata, scripts, and documentation.
