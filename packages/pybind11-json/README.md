<!-- SPDX-License-Identifier: Apache-2.0 -->
# pybind11-json

This directory packages upstream `https://github.com/pybind/pybind11_json` version `0.2.15` for openEuler 24.03 LTS SP3 on `riscv64`/RVA23.

Release 6 pins the official upstream release contents to immutable commit
`32043f433ed987b2c2ce99d689ec337bcbd4ba95` using
`https://codeload.github.com/pybind/pybind11_json/tar.gz/32043f433ed987b2c2ce99d689ec337bcbd4ba95`.
The archive SHA-256 is
`6a12673bea0e1af5039833016c86b6a9e2712f30c30108e63dd45260e572c425`;
its exact root is `pybind11_json-32043f433ed987b2c2ce99d689ec337bcbd4ba95`.
The complete 13-file contents match the independently verified legacy 0.2.15
tag archive (SHA-256 `9a4a1494549a2db27bc4c5a16743a5c88ebc18e13c73019c56f399ae0310baf2`).
Archive/Git blob identity and SHA-256 are verified; upstream did not provide a
detached signature. RPM preparation selects the exact immutable archive root.

`pybind11_json` is a header-only bridge whose installed CMake metadata has
public dependencies on pybind11 and nlohmann/json. The RPM therefore requires
the distribution `pybind11-devel` and `nlohmann-json3-devel` providers instead
of installing private copies of either dependency. GTest is a build-only
dependency for the upstream suite; Python headers are required at both build
time and installed-consumer runtime through `python3-devel`.

Upstream names its suite option `BUILD_TESTS` and exposes the resulting Google
Test executable without registering it with CTest. `%check` enables that exact
option and directly executes `test_pybind11_json`; installed smoke independently
consumes `find_package(pybind11_json)` and exercises a Python-dictionary to JSON
conversion and back in a compiled C++17 program.

Release 3 configures with openEuler's out-of-source `%cmake_conf` macro. This
keeps the configure directory aligned with `%cmake_build`, `%cmake_install`, and
the explicit `%check` executable path while leaving the upstream suite enabled.

Release 4 marks the installed header-only CMake package as `noarch`. The build
still compiles and executes the complete upstream test binary on the target
architecture; only the installed headers and CMake metadata are architecture
independent. Target CI produced RPM and SRPM artifacts and passed all 29 upstream
tests, but installed consumer compilation then failed because `Python.h` was not
installed.

Release 5 declares `python3-devel` as an installed dependency so consumers of
the exported `pybind11_json` CMake target receive the Python development headers
required by pybind11.

The latest release-5 attempt failed during official dependency preparation,
before compilation or default tests: metadata loading consumed 19 minutes and
7 seconds and both DNF attempts timed out. Its existing 3600-second dependency
cap is not increased. Release 6 is based on the current protected infrastructure,
whose pinned image preloads and validates official DNF metadata. Actual current
main logs show its embedded target verification succeeded; the cache transaction
JSON is not separately exported and this is not candidate build/test acceptance.

The full upstream suite (29 static test declarations) and installed compiled
C++/Python consumer remain unchanged. Upstream's optional Google Test download
stays off; the declared distribution GTest provider is used. Current reviewed
providers pybind11 2.11.1 and nlohmann/json 3.12.0 are inside upstream's documented
compatibility ranges (pybind11 >=2.2.4,<3.0 and nlohmann/json >=3.2.0,<4.0).
Release 6 target build, complete suite, installed consumer and publication still
require fresh CI and physical-product verification; historical release-4 results
above are not evidence for this release.

External source and patch licenses remain those of their respective upstream projects. The repository license only covers original packaging metadata, scripts, and documentation.
