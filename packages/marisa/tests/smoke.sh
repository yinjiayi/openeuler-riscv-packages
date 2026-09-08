#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- marisa marisa-devel
smoke_dir=$(mktemp -d)
trap 'rm -rf "$smoke_dir"' EXIT
cat >"$smoke_dir/smoke.cc" <<'EOF'
#include <marisa.h>
int main() {
    marisa::Keyset keys;
    keys.push_back("riscv");
    marisa::Trie trie;
    trie.build(keys);
    return trie.num_keys() == 1 ? 0 : 1;
}
EOF
c++ "$smoke_dir/smoke.cc" -lmarisa -o "$smoke_dir/smoke"
"$smoke_dir/smoke"
