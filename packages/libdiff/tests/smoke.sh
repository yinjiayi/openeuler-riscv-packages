#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- libdiff libdiff-devel
diffchars abc adc | grep -Fx 'Edit distance: 2'
diffwords 'alpha beta' 'alpha gamma' | grep -Fx 'Edit distance: 2'

smoke_dir=$(mktemp -d)
trap 'rm -rf "$smoke_dir"' EXIT
cat > "$smoke_dir/consumer.c" <<'EOF'
#include <stddef.h>
#include <stdlib.h>
#include <diff.h>

static int same(const void *left, const void *right) {
    return *(const char *)left == *(const char *)right;
}

int main(void) {
    const char left[] = "abc";
    const char right[] = "adc";
    struct diff result;
    if (diff(&result, same, sizeof(char), left, 3, right, 3) != 1)
        return 1;
    int ok = result.editdist == 2 && result.lcssz == 2;
    free(result.ses);
    free(result.lcs);
    return ok ? 0 : 2;
}
EOF
cc "$smoke_dir/consumer.c" -ldiff -o "$smoke_dir/consumer"
"$smoke_dir/consumer"
