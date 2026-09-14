<!-- SPDX-License-Identifier: Apache-2.0 -->
# qpdf

This directory packages upstream `https://github.com/qpdf/qpdf` version `12.3.2` for openEuler 24.03 LTS SP3 on `riscv64`/RVA23.

The package builds qpdf's command-line tools and shared `libqpdf` library. Static `libqpdf` is disabled using upstream's documented CMake option so the same library sources are not compiled twice under QEMU. The `%check` phase runs the complete seven-test upstream CTest suite, including its fuzz test; Perl is declared explicitly because qpdf's test driver uses it. A 180-minute package timeout retains that complete suite after a 120-minute run completed the first six tests but expired in the fuzz test. Installed smoke uses qpdf to create, inspect, and validate an empty PDF. Installed manual pages are excluded from the generated file manifest and owned through an RPM compression-tolerant glob because the standard post-install compression pass changes their suffixes after `%install`.

External source and patch licenses remain those of their respective upstream projects. The repository license only covers original packaging metadata, scripts, and documentation.
