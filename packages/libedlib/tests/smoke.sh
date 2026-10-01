#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- libedlib libedlib-devel
smoke_dir=$(mktemp -d)
trap 'rm -rf "$smoke_dir"' EXIT

cat > "$smoke_dir/consumer.c" <<'EOF'
#include <edlib.h>

int main(void) {
    EdlibAlignResult result = edlibAlign("kitten", 6, "sitting", 7,
                                         edlibDefaultAlignConfig());
    int ok = result.status == EDLIB_STATUS_OK && result.editDistance == 3;
    edlibFreeAlignResult(result);
    return ok ? 0 : 1;
}
EOF

cc "$smoke_dir/consumer.c" -ledlib -o "$smoke_dir/consumer"
"$smoke_dir/consumer"
