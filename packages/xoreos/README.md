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

Exact-head Package CI run `33694996938` for commit
`9271abdfc4ef23bf19d5902a2279e15c1fb62a5f` built successfully and passed all
82 tests. The install step created `/usr/share/man/man6/xoreos.6`, but RPM's
standard `brp-compress` processing renamed it after the generated file list had
recorded the uncompressed path, so `%files` could no longer find that entry.
Release 5 removes the raw man-page path from the generated list and declares it
with the compression-safe `%{_mandir}/man6/%{name}.6*` RPM convention. RPM
compression and the complete test suite remain enabled.

External source and patch licenses remain those of their respective upstream projects. The repository license only covers original packaging metadata, scripts, and documentation.
