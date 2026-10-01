<!-- SPDX-License-Identifier: Apache-2.0 -->
# rakarrack-plus

This directory packages upstream `https://github.com/Stazed/rakarrack-plus` version `1.4.1` for openEuler 24.03 LTS SP3 on `riscv64`/RVA23.

External source and patch licenses remain those of their respective upstream projects. The repository license only covers original packaging metadata, scripts, and documentation.

Release 6 lists the manual page separately with RPM's compression suffix
wildcard. Release 5 completed compilation and installation, but its generated
file list referenced the uncompressed manual page after `brp-compress` had
renamed it. The 120-minute budget and existing build features are retained.
Upstream 1.4.1 registered no CTest tests in the observed configuration;
the retained `%check` invocation is not evidence of a passing upstream suite.
