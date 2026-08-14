#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- libfyaml libfyaml-devel libfyaml-static
fy-tool --version | grep -Fx '0.9.6'
pkg-config --modversion libfyaml | grep -Fx '0.9.6'

smoke_dir=$(mktemp -d)
trap 'rm -rf -- "$smoke_dir"' EXIT
cat >"$smoke_dir/libfyaml-smoke.c" <<'EOF'
#include <libfyaml.h>
#include <string.h>

int main(void) {
    struct fy_document *document;
    struct fy_node *answer;
    const char *value;

    document = fy_document_build_from_string(NULL, "answer: 42\n", 11);
    if (document == NULL)
        return 1;
    answer = fy_node_mapping_lookup_by_string(fy_document_root(document),
                                               "answer", 6);
    value = answer != NULL ? fy_node_get_scalar0(answer) : NULL;
    if (value == NULL || strcmp(value, "42") != 0)
        return 2;
    fy_document_destroy(document);
    return 0;
}
EOF

cc "$smoke_dir/libfyaml-smoke.c" -o "$smoke_dir/libfyaml-smoke" \
  $({ pkg-config --cflags --libs libfyaml; })
"$smoke_dir/libfyaml-smoke"
