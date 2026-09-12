<!-- SPDX-License-Identifier: Apache-2.0 -->
# timepad

This directory packages upstream `https://github.com/agokule/timepad` version `0.1.0` for openEuler 24.03 LTS SP3 on `riscv64`/RVA23.

The build uses upstream's exact SDL and Dear ImGui revisions. Both secondary sources are supplied as independently SHA-256-verified archives, and CMake is run with FetchContent fully disconnected so an undeclared dependency download fails closed. SDL is linked statically with its X11 desktop backend, while the application, desktop entry, icon, fonts, and timer sound are installed under the standard system prefixes. The package reserves 120 minutes for dependency preparation and the complete SDL and Timepad build under QEMU.

RPM file-list entries are quoted so the upstream `Font Awesome 7` font filenames retain their spaces. Release 4 repairs the file-list parsing failure observed after compilation in CI run `34232688256`; it does not remove fonts, change the X11 backend, or remove existing checks. Release 5 closes the secondary-source provenance gap observed while auditing run `34687640099`; that run built, installed, and passed package smoke, while its non-required state-recording job alone hit the GitHub installation API rate limit. The installed smoke test checks both affected font paths. The 120-minute package budget replaces the earlier 90-minute limit after ordinary CI run `34703434622` spent 2,237 seconds preparing dependencies and then timed out at 99% compilation; the same exact head completed under trusted QEMU run `34703608126`, so the timeout is not treated as a source failure or native-only requirement. Upstream currently registers no CTest tests, so successful CI is bounded to compile, package, install, and product-file smoke evidence rather than an upstream test-suite claim.

External source and patch licenses remain those of their respective upstream projects. The repository license only covers original packaging metadata, scripts, and documentation.
