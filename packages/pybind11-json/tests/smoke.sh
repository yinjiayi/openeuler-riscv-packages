#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- pybind11-json
rpm -q -- pybind11-devel
rpm -q -- nlohmann-json3-devel

smoke_dir=$(mktemp -d)
trap 'rm -rf -- "$smoke_dir"' EXIT

cat >"$smoke_dir/CMakeLists.txt" <<'EOF'
cmake_minimum_required(VERSION 3.12)
project(pybind11_json_smoke LANGUAGES CXX)
find_package(pybind11_json 0.2.15 EXACT CONFIG REQUIRED)
add_executable(pybind11-json-smoke main.cpp)
target_compile_features(pybind11-json-smoke PRIVATE cxx_std_17)
target_link_libraries(pybind11-json-smoke PRIVATE
  pybind11_json
  pybind11::embed
  nlohmann_json::nlohmann_json)
EOF

cat >"$smoke_dir/main.cpp" <<'EOF'
#include <nlohmann/json.hpp>
#include <pybind11/embed.h>
#include <pybind11_json/pybind11_json.hpp>

namespace py = pybind11;

int main() {
    py::scoped_interpreter interpreter;
    py::dict object;
    object["target"] = "riscv64";
    object["value"] = 23;
    const nlohmann::json document = object;
    const py::object round_trip = document;
    return document.at("target") == "riscv64" &&
                   document.at("value") == 23 &&
                   round_trip.cast<py::dict>()["value"].cast<int>() == 23
               ? 0
               : 1;
}
EOF

cmake -S "$smoke_dir" -B "$smoke_dir/build"
cmake --build "$smoke_dir/build" --verbose
"$smoke_dir/build/pybind11-json-smoke"
