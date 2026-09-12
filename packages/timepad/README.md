<!-- SPDX-License-Identifier: Apache-2.0 -->
# timepad

This directory packages upstream `https://github.com/agokule/timepad` version `0.1.0` for openEuler 24.03 LTS SP3 on `riscv64`/RVA23.

The build uses upstream's pinned SDL and Dear ImGui revisions. SDL is linked statically with its X11 desktop backend, while the application, desktop entry, icon, fonts, and timer sound are installed under the standard system prefixes. The package reserves 90 minutes for the complete SDL and Timepad build under QEMU.

RPM file-list entries are quoted so the upstream `Font Awesome 7` font filenames retain their spaces. Release 4 repairs the file-list parsing failure observed after compilation in CI run `34232688256`; it does not remove fonts, change the X11 backend, or remove existing checks. The installed smoke test also checks both affected font paths. That run completed compilation, but CTest reported no registered tests, so it is not evidence of an upstream test suite passing.

External source and patch licenses remain those of their respective upstream projects. The repository license only covers original packaging metadata, scripts, and documentation.
