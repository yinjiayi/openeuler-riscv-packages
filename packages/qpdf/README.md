<!-- SPDX-License-Identifier: Apache-2.0 -->
# qpdf

This directory packages upstream `https://github.com/qpdf/qpdf` version `12.3.2` for openEuler 24.03 LTS SP3 on `riscv64`/RVA23.

The package builds qpdf's command-line tools and shared `libqpdf` library. Static `libqpdf` is disabled using upstream's documented CMake option so the same library sources are not compiled twice under QEMU. The `%check` phase runs the complete upstream CTest suite; Perl is declared explicitly because qpdf's test driver uses it. A 120-minute package timeout replaces the initial 60-minute limit that expired during duplicate library compilation without a compiler or test failure. Installed manual pages are excluded from the generated file manifest and owned through an RPM compression-tolerant glob because the standard post-install compression pass changes their suffixes after `%install`.

External source and patch licenses remain those of their respective upstream projects. The repository license only covers original packaging metadata, scripts, and documentation.
