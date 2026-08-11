#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- m4
actual=$(m4 <<'EOF'
define(`TARGET', `riscv64-RVA23')dnl
TARGET
EOF
)
test "$actual" = "riscv64-RVA23"
