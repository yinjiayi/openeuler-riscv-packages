#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- npth npth-devel
test "$(pkg-config --modversion npth)" = 1.8

smoke_dir=$(mktemp -d)
trap 'rm -rf "$smoke_dir"' EXIT
cat > "$smoke_dir/smoke.c" <<'EOF'
#include <npth.h>

static void *worker(void *argument)
{
    return argument;
}

int main(void)
{
    int value = 23;
    npth_t thread;
    void *result = NULL;

    if (npth_init() != 0) {
        return 1;
    }
    if (npth_create(&thread, NULL, worker, &value) != 0) {
        return 1;
    }
    if (npth_join(thread, &result) != 0 || result != &value) {
        return 1;
    }
    return 0;
}
EOF
gcc -Wall -Wextra -Werror "$smoke_dir/smoke.c" \
  $(pkg-config --cflags --libs npth) -o "$smoke_dir/smoke"
"$smoke_dir/smoke"
