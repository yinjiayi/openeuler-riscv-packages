#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- libusb libusb-devel
smoke_dir=$(mktemp -d)
trap 'rm -rf "$smoke_dir"' EXIT
cat >"$smoke_dir/smoke.c" <<'EOF'
#include <libusb-1.0/libusb.h>
int main(void) {
    libusb_context *context = 0;
    int result = libusb_init(&context);
    if (result != 0) return 1;
    libusb_exit(context);
    return 0;
}
EOF
cc "$smoke_dir/smoke.c" -lusb-1.0 -o "$smoke_dir/smoke"
"$smoke_dir/smoke"
