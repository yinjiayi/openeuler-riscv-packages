#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- libXrandr
pkg-config --modversion xrandr | grep -Fx '1.5.5'

smoke_dir=$(mktemp -d)
trap 'rm -rf -- "$smoke_dir"' EXIT

cat >"$smoke_dir/smoke.c" <<'EOF'
#include <string.h>
#include <X11/extensions/Xrandr.h>

int main(void)
{
    XRRModeInfo *mode = XRRAllocModeInfo("1280x720", 8);
    XRRCrtcGamma *gamma = XRRAllocGamma(3);
    XRRMonitorInfo *monitor = XRRAllocateMonitor(NULL, 2);
    int ok = mode && gamma && monitor &&
        mode->nameLength == 8 && strcmp(mode->name, "1280x720") == 0 &&
        gamma->size == 3 && gamma->green == gamma->red + 3 &&
        gamma->blue == gamma->green + 3 && monitor->noutput == 2;

    XRRFreeModeInfo(mode);
    XRRFreeGamma(gamma);
    XRRFreeMonitors(monitor);
    return ok ? 0 : 1;
}
EOF

${CC:-cc} -std=c99 -Wall -Wextra -Werror \
  $(pkg-config --cflags xrandr) \
  "$smoke_dir/smoke.c" $(pkg-config --libs xrandr) -o "$smoke_dir/smoke"
"$smoke_dir/smoke"
