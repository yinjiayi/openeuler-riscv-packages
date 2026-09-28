#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- libXv
pkg-config --modversion xv | grep -Fx '1.0.13'

smoke_dir=$(mktemp -d)
trap 'rm -rf -- "$smoke_dir"' EXIT

cat >"$smoke_dir/smoke.c" <<'EOF'
#include <stdlib.h>
#include <X11/Xlib.h>
#include <X11/extensions/Xvlib.h>

int main(void)
{
    XvAdaptorInfo *adaptors = calloc(1, sizeof(*adaptors));
    XvEncodingInfo *encodings = calloc(1, sizeof(*encodings));
    if (!adaptors || !encodings) {
        free(adaptors);
        free(encodings);
        return 1;
    }
    adaptors->num_adaptors = 1;
    encodings->num_encodings = 1;
    adaptors->name = calloc(1, 4);
    adaptors->formats = calloc(1, sizeof(*adaptors->formats));
    encodings->name = calloc(1, 4);
    if (!adaptors->name || !adaptors->formats || !encodings->name) {
        free(adaptors->name);
        free(adaptors->formats);
        free(encodings->name);
        free(adaptors);
        free(encodings);
        return 2;
    }
    XvFreeAdaptorInfo(adaptors);
    XvFreeEncodingInfo(encodings);
    XvFreeAdaptorInfo(NULL);
    XvFreeEncodingInfo(NULL);
    return 0;
}
EOF

${CC:-cc} -std=c99 -Wall -Wextra -Werror \
  $(pkg-config --cflags xv) \
  "$smoke_dir/smoke.c" $(pkg-config --libs xv) -o "$smoke_dir/smoke"
"$smoke_dir/smoke"
