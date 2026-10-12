#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- libconfini libconfini-devel
smoke_dir=$(mktemp -d)
trap 'rm -rf "$smoke_dir"' EXIT

printf '[sample]\nkey = expected\n' > "$smoke_dir/sample.ini"
cat > "$smoke_dir/smoke.c" <<'EOF'
#include <confini.h>
#include <string.h>

static int callback(IniDispatch *dispatch, void *context) {
    int *found = context;
    if (dispatch->type == INI_KEY &&
        strcmp(dispatch->append_to, "sample") == 0 &&
        strcmp(dispatch->data, "key") == 0 &&
        strcmp(dispatch->value, "expected") == 0) {
        *found = 1;
    }
    return 0;
}

int main(int argc, char **argv) {
    int found = 0;
    if (argc != 2) return 2;
    if (load_ini_path(argv[1], INI_DEFAULT_FORMAT, NULL, callback, &found)) return 3;
    return found ? 0 : 4;
}
EOF

cc "$smoke_dir/smoke.c" $(pkg-config --cflags --libs libconfini) -o "$smoke_dir/smoke"
"$smoke_dir/smoke" "$smoke_dir/sample.ini"
