#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- raptor2 raptor2-devel
rapper --version
smoke_dir=$(mktemp -d)
trap 'rm -rf -- "$smoke_dir"' EXIT
cat >"$smoke_dir/smoke.c" <<'EOF'
#include <raptor2/raptor2.h>

int main(void) {
    raptor_world *world = raptor_new_world();
    if (world == NULL) {
        return 1;
    }
    if (raptor_world_open(world) != 0) {
        raptor_free_world(world);
        return 2;
    }
    raptor_free_world(world);
    return 0;
}
EOF
cc "$smoke_dir/smoke.c" $(pkg-config --cflags --libs raptor2) -o "$smoke_dir/smoke"
"$smoke_dir/smoke"
