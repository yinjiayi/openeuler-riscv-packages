<!-- SPDX-License-Identifier: Apache-2.0 -->
# netperf

This directory packages upstream `https://github.com/HewlettPackard/netperf` version `2.7.0` for openEuler 24.03 LTS SP3 on `riscv64`/RVA23.

External source and patch licenses remain those of their respective upstream projects. The repository license only covers original packaging metadata, scripts, and documentation.

The downstream Linux declaration fix keeps the configure-detected
`sendfile`, `splice`, and CPU-affinity features enabled under GCC 14. It
combines the project-wide GNU feature-test-macro approach used by Fedora with
the missing Linux `sys/sendfile.h` include observed by openEuler RISC-V CI.
The UUID helper also carries the accepted upstream `unistd.h` include so its
`read` and `close` calls retain proper declarations.
The build uses Fedora's documented `-fcommon` compatibility workaround for
the duplicate tentative definitions in the 2.7.0 sources under GCC 10 and
later.
The RPM file list uses standard path macros and compression-safe suffixes for
the installed binaries, manual pages, and info document. The shared info
directory index generated during installation is removed from the buildroot;
it is owned and maintained by the system rather than by this package.
