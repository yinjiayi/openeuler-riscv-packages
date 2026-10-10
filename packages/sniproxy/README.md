<!-- SPDX-License-Identifier: Apache-2.0 -->
# sniproxy

This directory packages upstream `https://github.com/dlundquist/sniproxy` version `0.7.0` for openEuler 24.03 LTS SP3 on `riscv64`/RVA23.

External source and patch licenses remain those of their respective upstream projects. The repository license only covers original packaging metadata, scripts, and documentation.

The downstream test patches preserve the complete upstream test suite. They
skip only the transparent-proxy test when network namespaces are unavailable
and serialize child startup with PID registration to avoid a SIGCHLD race.
