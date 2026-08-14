#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- libsrtp libsrtp-devel
smoke_dir=$(mktemp -d)
trap 'rm -rf "$smoke_dir"' EXIT
cat >"$smoke_dir/smoke.c" <<'EOF'
#include <srtp2/srtp.h>
int main(void) {
    if (srtp_init() != srtp_err_status_ok) return 1;
    return srtp_shutdown() == srtp_err_status_ok ? 0 : 1;
}
EOF
cc "$smoke_dir/smoke.c" -lsrtp2 -o "$smoke_dir/smoke"
"$smoke_dir/smoke"
