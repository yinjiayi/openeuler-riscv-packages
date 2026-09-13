#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- unifdef
unifdef -V 2>&1 | grep -Fq '2.12'
smoke_dir=$(mktemp -d)
trap 'rm -rf -- "$smoke_dir"' EXIT
cat >"$smoke_dir/input.c" <<'EOF'
#ifdef ENABLED
int selected = 1;
#else
int selected = 0;
#endif
EOF
unifdef -x2 -DENABLED "$smoke_dir/input.c" >"$smoke_dir/output.c"
grep -Fq 'int selected = 1;' "$smoke_dir/output.c"
if grep -Fq 'int selected = 0;' "$smoke_dir/output.c"; then
  exit 1
fi
