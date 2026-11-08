#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- libsigsegv libsigsegv-devel
d=$(mktemp -d); trap 'rm -rf "$d"' EXIT
cat >"$d/smoke.c" <<'EOF'
#include <sigsegv.h>
static int handler(void *address, int serious) { (void)address; return serious ? 0 : 0; }
int main(void) { if (sigsegv_install_handler(handler) != 0) return 1; sigsegv_deinstall_handler(); return 0; }
EOF
cc -Wall -Werror "$d/smoke.c" -lsigsegv -o "$d/smoke"
"$d/smoke"
