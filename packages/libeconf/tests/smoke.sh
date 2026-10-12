#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- libeconf libeconf-devel
econftool -h 2>&1 | grep -F 'Usage: econftool'
rpm -ql libeconf-devel | grep -E '/pkgconfig/libeconf\.pc$'

smoke_dir=$(mktemp -d)
trap 'rm -rf -- "$smoke_dir"' EXIT
printf 'answer=42\n' >"$smoke_dir/example.conf"
cat >"$smoke_dir/smoke.c" <<'EOF'
#include <libeconf.h>
#include <stdlib.h>
#include <string.h>

int main(int argc, char **argv) {
    econf_file *file = NULL;
    char *value = NULL;
    if (argc != 2 || econf_readFile(&file, argv[1], "=", "#") != ECONF_SUCCESS)
        return 1;
    if (econf_getStringValue(file, NULL, "answer", &value) != ECONF_SUCCESS)
        return 2;
    int ok = strcmp(value, "42") == 0;
    free(value);
    econf_free(file);
    return ok ? 0 : 3;
}
EOF
cc "$smoke_dir/smoke.c" -leconf -o "$smoke_dir/smoke"
"$smoke_dir/smoke" "$smoke_dir/example.conf"
