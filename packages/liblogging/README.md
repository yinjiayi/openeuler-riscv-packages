<!-- SPDX-License-Identifier: Apache-2.0 -->
# liblogging

This directory packages upstream `https://liblogging.org/` version `1.0.6` for openEuler 24.03 LTS SP3 on `riscv64`/RVA23.

The full upstream `make check` target and the explicit standard-logging tester run in `%check`. Installed smoke checks that both versioned shared-library links exist and belong to the installed `liblogging` RPM. Upstream's `stdlog/Makefile.am` declares libtool `-version-info 1:0:1` and `rfc3195/src/Makefile.am` declares `0:0:0`; both therefore have ABI major `0`. The previous `.so.1` expectation for stdlog did not match that source contract or the successful RPM manifest.

External source and patch licenses remain those of their respective upstream projects. The repository license only covers original packaging metadata, scripts, and documentation.
