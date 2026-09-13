<!-- SPDX-License-Identifier: Apache-2.0 -->
# selint

This directory packages upstream `https://github.com/SELinuxProject/selint` version `1.5.1` for openEuler 24.03 LTS SP3 on `riscv64`/RVA23.

Release 2 declares the complete build-time dependency set used by upstream's
Autotools configuration: Flex and Bison generate the parser, libconfuse and
uthash provide required interfaces, help2man generates the manual, and the
enabled Check-based upstream test suite continues to run during `%check`.

Release 3 increases the package build timeout from 60 to 180 minutes. The
previous exact-head CI run resolved all 216 required packages but exhausted
the old budget while downloading that target-native dependency closure under
QEMU. This change does not remove dependencies, tests, or packaged features.

Release 4 keeps the installed manual page in the package with an RPM-safe
compression glob outside the pre-compression dynamic file list. Exact-head CI
completed the build and passed all 18 upstream tests, but RPM's `brp-compress`
renamed `selint.1` before file collection, so the earlier literal dynamic entry
no longer existed. No test, manual, dependency, or feature is removed, and the
RISC-V build status remains `unknown` pending successful RPM and installed-smoke
evidence.

External source and patch licenses remain those of their respective upstream projects. The repository license only covers original packaging metadata, scripts, and documentation.
