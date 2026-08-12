#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- protobuf-c protobuf-c-devel
protoc-c --version 2>&1 | grep -F 'protobuf-c 1.5.2'

smoke_dir=$(mktemp -d)
trap 'rm -rf "$smoke_dir"' EXIT
cat >"$smoke_dir/message.proto" <<'EOF'
syntax = "proto3";
message SmokeMessage {
  string value = 1;
}
EOF
protoc-c --proto_path="$smoke_dir" --c_out="$smoke_dir" "$smoke_dir/message.proto"
test -s "$smoke_dir/message.pb-c.c"
test -s "$smoke_dir/message.pb-c.h"

cat >"$smoke_dir/protobuf-c-smoke.c" <<'EOF'
#include <protobuf-c/protobuf-c.h>
#include <string.h>

int main(void) {
    return strcmp(protobuf_c_version(), "1.5.2") != 0 ||
           protobuf_c_version_number() != 1005002;
}
EOF
cc $({ pkg-config --cflags libprotobuf-c; }) \
  "$smoke_dir/protobuf-c-smoke.c" -o "$smoke_dir/protobuf-c-smoke" \
  $({ pkg-config --libs libprotobuf-c; })
"$smoke_dir/protobuf-c-smoke"
