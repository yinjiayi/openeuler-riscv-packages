#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- libdvbpsi libdvbpsi-devel
smoke_dir=$(mktemp -d)
trap 'rm -rf "$smoke_dir"' EXIT

cat >"$smoke_dir/smoke.c" <<'EOF'
#include <stdint.h>
#include <stdbool.h>
#include <stddef.h>
#include <sys/types.h>
#include <dvbpsi/dvbpsi.h>
#include <dvbpsi/descriptor.h>

int main(void) {
    uint8_t payload[] = {0x12, 0x34};
    dvbpsi_t *decoder = dvbpsi_new(0, DVBPSI_MSG_ERROR);
    dvbpsi_descriptor_t *descriptor;
    int ok;
    if (!decoder) return 1;
    descriptor = dvbpsi_NewDescriptor(0x40, sizeof(payload), payload);
    if (!descriptor) return 2;
    ok = descriptor->i_tag == 0x40 && descriptor->i_length == sizeof(payload) &&
         descriptor->p_data[0] == payload[0] && descriptor->p_data[1] == payload[1];
    dvbpsi_DeleteDescriptors(descriptor);
    dvbpsi_delete(decoder);
    return ok ? 0 : 3;
}
EOF

cc "$smoke_dir/smoke.c" $(pkg-config --cflags --libs libdvbpsi) -o "$smoke_dir/smoke"
"$smoke_dir/smoke"
