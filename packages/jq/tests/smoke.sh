#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- jq jq-devel jq-help
test "$(jq --version)" = "jq-1.8.2"
test "$(printf '%s\n' '{"items":[3,1,2]}' | jq -c '.items | sort | map(. * 2)')" = \
  '[2,4,6]'

smoke_dir=$(mktemp -d)
trap 'rm -rf "$smoke_dir"' EXIT
cat >"$smoke_dir/libjq-smoke.c" <<'EOF'
#include <jq.h>

int main(void) {
    jq_state *state = jq_init();
    if (state == NULL) {
        return 1;
    }
    jq_teardown(&state);
    return state == NULL ? 0 : 2;
}
EOF
cc $({ pkg-config --cflags libjq; }) "$smoke_dir/libjq-smoke.c" \
  -o "$smoke_dir/libjq-smoke" $({ pkg-config --libs libjq; })
"$smoke_dir/libjq-smoke"
