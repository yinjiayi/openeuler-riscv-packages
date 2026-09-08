#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- jsoncpp jsoncpp-devel
smoke_dir=$(mktemp -d)
trap 'rm -rf "$smoke_dir"' EXIT
cat >"$smoke_dir/smoke.cc" <<'EOF'
#include <json/json.h>
#include <memory>
#include <string>
int main() {
    Json::CharReaderBuilder builder;
    std::unique_ptr<Json::CharReader> reader(builder.newCharReader());
    Json::Value root;
    std::string errors;
    const char text[] = "{\"arch\":\"riscv64\"}";
    return reader->parse(text, text + sizeof(text) - 1, &root, &errors) && root["arch"] == "riscv64" ? 0 : 1;
}
EOF
c++ "$smoke_dir/smoke.cc" -ljsoncpp -o "$smoke_dir/smoke"
"$smoke_dir/smoke"
