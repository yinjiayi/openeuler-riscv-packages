#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- hiredis hiredis-devel
smoke_dir=$(mktemp -d)
trap 'rm -rf "$smoke_dir"' EXIT
cat >"$smoke_dir/smoke.c" <<'EOF'
#include <hiredis/hiredis.h>
int main(void) {
    redisReader *reader = redisReaderCreate();
    if (reader == 0) return 1;
    redisReaderFree(reader);
    return 0;
}
EOF
cc "$smoke_dir/smoke.c" -lhiredis -o "$smoke_dir/smoke"
"$smoke_dir/smoke"
