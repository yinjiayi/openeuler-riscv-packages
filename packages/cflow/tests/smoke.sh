#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- cflow
cflow --version | grep -F 'cflow (GNU cflow) 1.8'

smoke_dir=$(mktemp -d)
trap 'rm -rf "$smoke_dir"' EXIT
cat >"$smoke_dir/cflow-smoke.c" <<'EOF'
static int helper(void) {
    return 42;
}

int main(void) {
    return helper() == 42 ? 0 : 1;
}
EOF
cflow --no-preprocess "$smoke_dir/cflow-smoke.c" >"$smoke_dir/callgraph"
grep -F 'main()' "$smoke_dir/callgraph"
grep -F 'helper()' "$smoke_dir/callgraph"
