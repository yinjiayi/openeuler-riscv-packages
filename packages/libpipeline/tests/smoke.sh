#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- libpipeline libpipeline-devel
smoke_dir=$(mktemp -d)
trap 'rm -rf "$smoke_dir"' EXIT

cat >"$smoke_dir/smoke.c" <<'EOF'
#include <pipeline.h>
#include <stddef.h>
#include <string.h>

int main(void) {
    pipeline *p = pipeline_new_command_args("printf", "pipeline-smoke\n", NULL);
    pipeline_want_out(p, -1);
    pipeline_start(p);
    const char *line = pipeline_readline(p);
    int result = (!line || strcmp(line, "pipeline-smoke\n") != 0);
    pipeline_free(p);
    return result;
}
EOF

cc "$smoke_dir/smoke.c" -lpipeline -o "$smoke_dir/smoke"
"$smoke_dir/smoke"
