#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- libmpc libmpc-devel libmpc-help
pkg-config --modversion mpc | grep -Fx '1.4.1'

smoke_dir=$(mktemp -d)
trap 'rm -rf "$smoke_dir"' EXIT
cat >"$smoke_dir/mpc-smoke.c" <<'EOF'
#include <mpc.h>
#include <string.h>

int main(void) {
    mpc_t value;
    int failed = strcmp(MPC_VERSION_STRING, "1.4.1") != 0;
    mpc_init2(value, 128);
    failed |= mpc_set_ui_ui(value, 1, 2, MPC_RNDNN) != 0;
    failed |= mpc_cmp_si_si(value, 1, 2) != 0;
    mpc_clear(value);
    return failed;
}
EOF
read -r -a mpc_flags <<<"$(pkg-config --cflags --libs mpc)"
cc "$smoke_dir/mpc-smoke.c" "${mpc_flags[@]}" -o "$smoke_dir/mpc-smoke"
"$smoke_dir/mpc-smoke"
