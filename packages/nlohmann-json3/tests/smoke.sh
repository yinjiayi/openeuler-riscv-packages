#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- nlohmann-json3-devel
for capability in \
  nlohmann-json3 \
  json-devel \
  nlohmann-json-devel \
  nlohmann_json-devel \
  'cmake(nlohmann_json)' \
  'pkgconfig(nlohmann_json)'; do
  rpm -q --whatprovides "$capability"
done
test "$(pkg-config --modversion nlohmann_json)" = 3.12.0
test -r /usr/share/cmake/nlohmann_json/nlohmann_jsonConfig.cmake

smoke_dir=$(mktemp -d)
trap 'rm -rf -- "$smoke_dir"' EXIT
cat >"$smoke_dir/smoke.cpp" <<'EOF'
#include <nlohmann/json.hpp>

#include <cstdint>
#include <vector>

int main() {
    using nlohmann::json;
    const json input = json::parse(R"({"target":"riscv64","value":23})");
    const std::vector<std::uint8_t> message_pack = json::to_msgpack(input);
    const json output = json::from_msgpack(message_pack);
    return output == input && output.at("value") == 23 ? 0 : 1;
}
EOF

read -r -a json_flags <<<"$(pkg-config --cflags nlohmann_json)"
c++ -std=c++17 "$smoke_dir/smoke.cpp" "${json_flags[@]}" \
  -o "$smoke_dir/smoke"
"$smoke_dir/smoke"
