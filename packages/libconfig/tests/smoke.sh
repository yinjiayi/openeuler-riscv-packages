#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- libconfig libconfig-devel
smoke_dir=$(mktemp -d)
trap 'rm -rf "$smoke_dir"' EXIT

cat >"$smoke_dir/smoke.c" <<'EOF'
#include <libconfig.h>

int main(void) {
    config_t config;
    int answer = 0;
    config_init(&config);
    if (!config_read_string(&config, "answer = 42;"))
        return 1;
    if (!config_lookup_int(&config, "answer", &answer))
        return 2;
    config_destroy(&config);
    return answer == 42 ? 0 : 3;
}
EOF

cat >"$smoke_dir/smoke.cc" <<'EOF'
#include <libconfig.h++>

int main() {
    libconfig::Config config;
    config.readString("answer = 42;");
    int answer = config.lookup("answer");
    return answer == 42 ? 0 : 1;
}
EOF

cc "$smoke_dir/smoke.c" -lconfig -o "$smoke_dir/smoke-c"
c++ "$smoke_dir/smoke.cc" -lconfig++ -o "$smoke_dir/smoke-cxx"
"$smoke_dir/smoke-c"
"$smoke_dir/smoke-cxx"
