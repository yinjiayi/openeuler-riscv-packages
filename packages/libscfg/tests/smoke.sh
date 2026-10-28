#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- libscfg libscfg-devel
pkg-config --modversion scfg | grep -Fx '0.2.0'

smoke_dir=$(mktemp -d)
trap 'rm -rf -- "$smoke_dir"' EXIT

cat >"$smoke_dir/smoke.c" <<'EOF'
#include <scfg.h>
#include <stdio.h>
#include <string.h>

int main(void) {
    struct scfg_block block = {0};
    FILE *input = tmpfile();
    int rc;

    if (input == NULL)
        return 1;
    if (fputs("server example.org\n", input) == EOF) {
        fclose(input);
        return 2;
    }
    rewind(input);
    rc = scfg_parse_file(&block, input);
    fclose(input);
    if (rc != 0 || block.directives_len != 1 ||
        strcmp(block.directives[0].name, "server") != 0 ||
        block.directives[0].params_len != 1 ||
        strcmp(block.directives[0].params[0], "example.org") != 0) {
        scfg_block_finish(&block);
        return 3;
    }
    scfg_block_finish(&block);
    return 0;
}
EOF

cc "$smoke_dir/smoke.c" -o "$smoke_dir/smoke" \
  $({ pkg-config --cflags --libs scfg; })
"$smoke_dir/smoke"
