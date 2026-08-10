#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- pugixml pugixml-devel
task_dir=$(mktemp -d)
trap 'rm -rf -- "$task_dir"' EXIT
cat >"$task_dir/smoke.cpp" <<'CPP'
#include <pugixml.hpp>
int main() {
  pugi::xml_document doc;
  return doc.load_string("<riscv bits='64'/>") &&
         doc.child("riscv").attribute("bits").as_int() == 64 ? 0 : 1;
}
CPP
g++ -std=c++11 "$task_dir/smoke.cpp" -lpugixml -o "$task_dir/smoke"
"$task_dir/smoke"
