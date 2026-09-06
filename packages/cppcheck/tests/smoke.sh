#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- cppcheck
cppcheck --version | grep -Fx 'Cppcheck 2.21.1'

smoke_dir=$(mktemp -d)
trap 'rm -rf "$smoke_dir"' EXIT
cat >"$smoke_dir/null.c" <<'EOF'
int dereference_null(void) {
    int *pointer = 0;
    return *pointer;
}
EOF

set +e
cppcheck --enable=warning --error-exitcode=2 "$smoke_dir/null.c" 2>"$smoke_dir/result"
status=$?
set -e
test "$status" -eq 2
grep -F '[nullPointer]' "$smoke_dir/result"
