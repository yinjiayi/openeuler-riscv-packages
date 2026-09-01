<!-- SPDX-License-Identifier: Apache-2.0 -->
# tnef

This directory packages upstream `https://github.com/verdammelt/tnef` version `1.4.18` for openEuler 24.03 LTS SP3 on `riscv64`/RVA23.

Release `2` keeps the complete upstream `make check` suite enabled and runs it
serially. Multiple command-line cases create and remove the same `AUTHORS`
output fixture, so parallel execution can alter `debug.test` output even when
the parser and extraction behavior are correct; serialization preserves every
test while preventing that shared-fixture race. The RPM file manifest
uses the standard compressed-man-page glob so the installed `tnef(1)` page
remains owned after openEuler's post-install compression step.

External source and patch licenses remain those of their respective upstream projects. The repository license only covers original packaging metadata, scripts, and documentation.
