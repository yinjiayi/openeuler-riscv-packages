<!-- SPDX-License-Identifier: Apache-2.0 -->
# pybind11-json

This directory packages upstream `https://github.com/pybind/pybind11_json` version `0.2.15` for openEuler 24.03 LTS SP3 on `riscv64`/RVA23.

The official tag archive is pinned to SHA-256
`9a4a1494549a2db27bc4c5a16743a5c88ebc18e13c73019c56f399ae0310baf2`.
Its single top-level directory is `pybind11_json-0.2.15`; RPM preparation
selects that exact root rather than deriving a hyphenated directory from the
RPM name.

`pybind11_json` is a header-only bridge whose installed CMake metadata has
public dependencies on pybind11 and nlohmann/json. The RPM therefore requires
the distribution `pybind11-devel` and `nlohmann-json3-devel` providers instead
of installing private copies of either dependency. GTest and Python headers are
declared build-only dependencies for the upstream suite.

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

External source and patch licenses remain those of their respective upstream projects. The repository license only covers original packaging metadata, scripts, and documentation.
