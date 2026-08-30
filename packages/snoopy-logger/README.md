<!-- SPDX-License-Identifier: Apache-2.0 -->
# snoopy-logger

This directory packages upstream `https://github.com/a2o/snoopy` version `2.5.2` for openEuler 24.03 LTS SP3 on `riscv64`/RVA23.

Packaging release `3` uses the verified `snoopy-snoopy-2.5.2` archive root and declares the hostname and process utilities required by the upstream suite. Exact-head CI also showed that `datasource_timestamp_us.sh` enforces a 5-50 millisecond wall-clock window around emulated target executions; that timing-sensitive check requires native RVA23 validation and is not treated as a QEMU build success.

External source and patch licenses remain those of their respective upstream projects. The repository license only covers original packaging metadata, scripts, and documentation.
