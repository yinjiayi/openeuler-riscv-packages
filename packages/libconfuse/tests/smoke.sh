#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- libconfuse libconfuse-devel
smoke_dir=$(mktemp -d)
trap 'rm -rf "$smoke_dir"' EXIT
cat >"$smoke_dir/smoke.c" <<'EOF'
#include <confuse.h>
int main(void) {
    cfg_opt_t options[] = {CFG_END()};
    cfg_t *configuration = cfg_init(options, 0);
    if (configuration == 0) return 1;
    cfg_free(configuration);
    return 0;
}
EOF
cc "$smoke_dir/smoke.c" -lconfuse -o "$smoke_dir/smoke"
"$smoke_dir/smoke"
