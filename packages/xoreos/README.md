<!-- SPDX-License-Identifier: Apache-2.0 -->
# xoreos

This directory packages upstream `https://github.com/xoreos/xoreos` version `0.0.6` for openEuler 24.03 LTS SP3 on `riscv64`/RVA23.

Exact-head Package CI run `33671482882` completed dependency preparation in 311 seconds, then compiled under QEMU for the remaining 2,989 seconds and reached 44% before the 60-minute package budget expired. The build log contained no concrete compiler or test failure. Release 3 therefore raises only the bounded package timeout to 180 minutes; the complete build and `%check` remain enabled and unchanged.

Exact-head Package CI run `33678267402` for commit
`406fe3b17539ccd3e05737e382da9e0e127a5178` completed the full build and
install phases, then direct `ctest` execution reported all 82 registered tests
as `Not Run` because upstream deliberately marks their binaries
`EXCLUDE_FROM_ALL`. Release 4 builds upstream's custom `check` target, which
explicitly depends on every excluded test target before it runs `ctest`; no
test is disabled or skipped.

External source and patch licenses remain those of their respective upstream projects. The repository license only covers original packaging metadata, scripts, and documentation.
