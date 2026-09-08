#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- oniguruma oniguruma-devel
smoke_dir=$(mktemp -d)
trap 'rm -rf "$smoke_dir"' EXIT
cat >"$smoke_dir/smoke.c" <<'EOF'
#include <oniguruma.h>
#include <string.h>
int main(void) {
    OnigRegex regex;
    OnigErrorInfo error;
    const OnigUChar pattern[] = "RISC-V[0-9]+";
    const OnigUChar text[] = "openEuler RISC-V64";
    if (onig_new(&regex, pattern, pattern + strlen((const char *)pattern),
                 ONIG_OPTION_NONE, ONIG_ENCODING_UTF8, ONIG_SYNTAX_DEFAULT,
                 &error) != ONIG_NORMAL) return 1;
    OnigRegion *region = onig_region_new();
    int result = onig_search(regex, text, text + strlen((const char *)text),
                             text, text + strlen((const char *)text), region,
                             ONIG_OPTION_NONE);
    onig_region_free(region, 1);
    onig_free(regex);
    onig_end();
    return result >= 0 ? 0 : 2;
}
EOF
cc "$smoke_dir/smoke.c" -lonig -o "$smoke_dir/smoke"
"$smoke_dir/smoke"
