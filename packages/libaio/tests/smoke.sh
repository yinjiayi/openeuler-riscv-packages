#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- libaio libaio-devel
smoke_dir=$(mktemp -d)
trap 'rm -rf "$smoke_dir"' EXIT
cat >"$smoke_dir/smoke.c" <<'EOF'
#include <libaio.h>
int main(void) {
    io_context_t context = 0;
    if (io_queue_init(1, &context) != 0) return 1;
    return io_queue_release(context) == 0 ? 0 : 2;
}
EOF
cc "$smoke_dir/smoke.c" -laio -o "$smoke_dir/smoke"
"$smoke_dir/smoke"
