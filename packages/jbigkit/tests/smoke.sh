#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- jbigkit jbigkit-libs jbigkit-devel

smoke_dir=$(mktemp -d)
trap 'rm -rf "$smoke_dir"' EXIT

cat >"$smoke_dir/smoke.c" <<'EOF'
#include <jbig.h>
#include <jbig85.h>

int main(void) {
    if (JBG_VERSION_MAJOR != 2 || JBG_VERSION_MINOR != 1)
        return 1;
    if (jbg_strerror(JBG_EOK) == 0 || jbg85_strerror(0) == 0)
        return 2;
    return 0;
}
EOF

cc "$smoke_dir/smoke.c" -ljbig -ljbig85 -o "$smoke_dir/smoke"
"$smoke_dir/smoke"

printf 'P4\n8 1\n\252' >"$smoke_dir/input.pbm"
pbmtojbg "$smoke_dir/input.pbm" "$smoke_dir/image.jbg"
jbgtopbm "$smoke_dir/image.jbg" "$smoke_dir/output.pbm"
cmp "$smoke_dir/input.pbm" "$smoke_dir/output.pbm"
