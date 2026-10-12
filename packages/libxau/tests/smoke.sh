#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- libXau libXau-devel
pkg-config --modversion xau | grep -Fx '1.0.12'

smoke_dir=$(mktemp -d)
trap 'rm -rf "$smoke_dir"' EXIT

cat >"$smoke_dir/smoke.c" <<'EOF'
#include <X11/Xauth.h>
#include <stdio.h>
#include <string.h>

int main(void) {
    char name[] = "MIT-MAGIC-COOKIE-1";
    char data[] = "0123456789abcdef";
    char empty[] = "";
    Xauth original = {0};
    Xauth *readback;
    FILE *stream = tmpfile();
    int result = 0;

    if (!stream) return 1;
    original.family = FamilyLocal;
    original.address = empty;
    original.number = empty;
    original.name_length = sizeof(name) - 1;
    original.name = name;
    original.data_length = sizeof(data) - 1;
    original.data = data;
    if (!XauWriteAuth(stream, &original)) result = 2;
    if (!result && fseek(stream, 0, SEEK_SET) != 0) result = 3;
    readback = result ? NULL : XauReadAuth(stream);
    if (!result && !readback) result = 4;
    if (!result && (readback->family != FamilyLocal ||
                    readback->name_length != sizeof(name) - 1 ||
                    readback->data_length != sizeof(data) - 1 ||
                    memcmp(readback->name, name, sizeof(name) - 1) != 0 ||
                    memcmp(readback->data, data, sizeof(data) - 1) != 0)) result = 5;
    if (readback) XauDisposeAuth(readback);
    fclose(stream);
    return result;
}
EOF

cc "$smoke_dir/smoke.c" $(pkg-config --cflags --libs xau) -o "$smoke_dir/smoke"
"$smoke_dir/smoke"
