<!-- SPDX-License-Identifier: Apache-2.0 -->
# netperf

This directory packages upstream `https://github.com/HewlettPackard/netperf` version `2.7.0` for openEuler 24.03 LTS SP3 on `riscv64`/RVA23.

External source and patch licenses remain those of their respective upstream projects. The repository license only covers original packaging metadata, scripts, and documentation.

The downstream Linux declaration fix keeps the configure-detected
`sendfile`, `splice`, and CPU-affinity features enabled under GCC 14. It
combines the project-wide GNU feature-test-macro approach used by Fedora with
the missing Linux `sys/sendfile.h` include observed by openEuler RISC-V CI.
