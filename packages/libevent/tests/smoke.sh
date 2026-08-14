#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- libevent libevent-devel
smoke_dir=$(mktemp -d)
trap 'rm -rf "$smoke_dir"' EXIT
cat >"$smoke_dir/smoke.c" <<'EOF'
#include <event2/event.h>
int main(void) {
    struct event_base *base = event_base_new();
    if (base == 0) return 1;
    event_base_free(base);
    return 0;
}
EOF
cc "$smoke_dir/smoke.c" -levent -o "$smoke_dir/smoke"
"$smoke_dir/smoke"
