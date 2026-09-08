#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- hyphen hyphen-devel
smoke_dir=$(mktemp -d)
trap 'rm -rf "$smoke_dir"' EXIT
cat >"$smoke_dir/smoke.c" <<'EOF'
#include <hyphen.h>
int main(void) {
    HyphenDict *dictionary = hnj_hyphen_load("/usr/share/hyphen/hyph_en_US.dic");
    if (dictionary == 0) return 1;
    hnj_hyphen_free(dictionary);
    return 0;
}
EOF
cc "$smoke_dir/smoke.c" -lhyphen -o "$smoke_dir/smoke"
"$smoke_dir/smoke"
