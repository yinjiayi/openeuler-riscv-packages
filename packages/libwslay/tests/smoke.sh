#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- libwslay libwslay-devel libwslay-static
smoke_dir=$(mktemp -d)
trap 'rm -rf -- "$smoke_dir"' EXIT
cat >"$smoke_dir/smoke.c" <<'EOF'
#include <wslay/wslay.h>
#include <wslay/wslayver.h>

#include <stddef.h>
#include <string.h>

int main(void) {
    struct wslay_event_callbacks callbacks = {0};
    wslay_event_context_ptr context = NULL;
    const int result = wslay_event_context_server_init(&context, &callbacks, NULL);

    if (result != 0 || context == NULL || strcmp(WSLAY_VERSION, "1.1.1") != 0) {
        return 1;
    }
    wslay_event_context_free(context);
    return 0;
}
EOF
cc "$smoke_dir/smoke.c" $(pkg-config --cflags --libs libwslay) -o "$smoke_dir/smoke"
"$smoke_dir/smoke"
