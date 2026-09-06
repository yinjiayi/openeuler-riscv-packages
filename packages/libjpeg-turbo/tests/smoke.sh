#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- libjpeg-turbo libjpeg-turbo-utils libjpeg-turbo-devel libjpeg-turbo-help
cjpeg -version 2>&1 | grep -F '3.2.0'
pkg-config --modversion libturbojpeg | grep -Fx '3.2.0'

smoke_dir=$(mktemp -d)
trap 'rm -rf "$smoke_dir"' EXIT
printf 'P3\n2 1\n255\n255 0 0 0 255 0\n' >"$smoke_dir/input.ppm"
cjpeg -quality 90 -outfile "$smoke_dir/output.jpg" "$smoke_dir/input.ppm"
test "$(od -An -tx1 -N2 "$smoke_dir/output.jpg" | tr -d ' \n')" = 'ffd8'
djpeg -ppm -outfile "$smoke_dir/output.ppm" "$smoke_dir/output.jpg"
head -n 1 "$smoke_dir/output.ppm" | grep -Fx 'P6'

cat >"$smoke_dir/turbojpeg-smoke.c" <<'EOF'
#include <turbojpeg.h>

int main(void) {
    tjhandle handle = tj3Init(TJINIT_COMPRESS);
    if (handle == NULL) {
        return 1;
    }
    tj3Destroy(handle);
    return 0;
}
EOF
cc $({ pkg-config --cflags libturbojpeg; }) "$smoke_dir/turbojpeg-smoke.c" \
  -o "$smoke_dir/turbojpeg-smoke" $({ pkg-config --libs libturbojpeg; })
"$smoke_dir/turbojpeg-smoke"
