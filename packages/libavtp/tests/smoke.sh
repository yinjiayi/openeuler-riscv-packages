#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- libavtp libavtp-devel
pkg-config --modversion avtp | grep -Fx '0.2.0'

smoke_dir=$(mktemp -d)
trap 'rm -rf -- "$smoke_dir"' EXIT
cat >"$smoke_dir/libavtp-smoke.c" <<'EOF'
#include <stdint.h>
#include <string.h>
#include <avtp.h>

int main(void) {
    struct avtp_common_pdu pdu;
    uint32_t value = 0;

    memset(&pdu, 0, sizeof(pdu));
    if (avtp_pdu_set(&pdu, AVTP_FIELD_SUBTYPE, AVTP_SUBTYPE_AAF) != 0)
        return 1;
    if (avtp_pdu_get(&pdu, AVTP_FIELD_SUBTYPE, &value) != 0)
        return 2;
    return value == AVTP_SUBTYPE_AAF ? 0 : 3;
}
EOF
cc "$smoke_dir/libavtp-smoke.c" -o "$smoke_dir/libavtp-smoke" \
  $({ pkg-config --cflags --libs avtp; })
"$smoke_dir/libavtp-smoke"
