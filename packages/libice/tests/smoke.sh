#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- libICE libICE-devel
pkg-config --modversion ice | grep -Fx '1.1.2'

smoke_dir=$(mktemp -d)
trap 'rm -rf "$smoke_dir"' EXIT

cat >"$smoke_dir/smoke.c" <<'EOF'
#include <X11/ICE/ICElib.h>
#include <X11/ICE/ICEutil.h>
#include <stdio.h>
#include <string.h>

int main(void) {
    char payload[] = "abcdef";
    char empty[] = "";
    IceAuthFileEntry original = {0};
    IceAuthFileEntry *readback = NULL;
    FILE *stream = tmpfile();
    int result = 0;
    if (!stream) return 1;
    original.protocol_name = "ICE";
    original.protocol_data = empty;
    original.network_id = "local/0";
    original.auth_name = "MIT-MAGIC-COOKIE-1";
    original.auth_data_length = sizeof(payload) - 1;
    original.auth_data = payload;
    if (!IceWriteAuthFileEntry(stream, &original)) result = 2;
    if (!result && fseek(stream, 0, SEEK_SET) != 0) result = 3;
    if (!result) readback = IceReadAuthFileEntry(stream);
    if (!result && !readback) result = 4;
    if (!result && (strcmp(readback->protocol_name, "ICE") != 0 ||
                    strcmp(readback->network_id, "local/0") != 0 ||
                    strcmp(readback->auth_name, "MIT-MAGIC-COOKIE-1") != 0 ||
                    readback->auth_data_length != sizeof(payload) - 1 ||
                    memcmp(readback->auth_data, payload, sizeof(payload) - 1) != 0)) result = 5;
    IceFreeAuthFileEntry(readback);
    fclose(stream);
    return result;
}
EOF

cc "$smoke_dir/smoke.c" $(pkg-config --cflags --libs ice) -o "$smoke_dir/smoke"
"$smoke_dir/smoke"
