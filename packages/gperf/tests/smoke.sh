#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- gperf
gperf --version | head -n 1 | grep -Fx 'GNU gperf 3.3'
smoke_dir=$(mktemp -d)
trap 'rm -rf "$smoke_dir"' EXIT

cat >"$smoke_dir/keywords.gperf" <<'EOF'
%{
#include <stddef.h>
#include <string.h>
%}
struct keyword { const char *name; int code; };
%%
riscv64, 64
rva23, 23
%%
EOF

gperf --language=C --struct-type --readonly-table --lookup-function-name=lookup_keyword \
  "$smoke_dir/keywords.gperf" >"$smoke_dir/generated.c"
cat >"$smoke_dir/smoke.c" <<'EOF'
#include <string.h>
#include "generated.c"

int main(void) {
    const struct keyword *entry = lookup_keyword("rva23", strlen("rva23"));
    return entry != NULL && entry->code == 23 ? 0 : 1;
}
EOF

cc "$smoke_dir/smoke.c" -o "$smoke_dir/smoke"
"$smoke_dir/smoke"
