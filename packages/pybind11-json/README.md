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

External source and patch licenses remain those of their respective upstream projects. The repository license only covers original packaging metadata, scripts, and documentation.
