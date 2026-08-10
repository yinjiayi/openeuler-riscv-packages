#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- fstrm fstrm-devel
command -v fstrm_capture fstrm_dump fstrm_replay >/dev/null
smoke_dir=$(mktemp -d)
trap 'rm -rf "$smoke_dir"' EXIT
cat >"$smoke_dir/smoke.c" <<'EOF'
#include <fstrm.h>
int main(void) {
    struct fstrm_control *control = fstrm_control_init();
    if (control == 0) return 1;
    fstrm_control_destroy(&control);
    return control == 0 ? 0 : 1;
}
EOF
cc "$smoke_dir/smoke.c" -lfstrm -o "$smoke_dir/smoke"
"$smoke_dir/smoke"
