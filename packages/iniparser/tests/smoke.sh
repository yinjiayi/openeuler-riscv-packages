#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- iniparser iniparser-devel
smoke_dir=$(mktemp -d)
trap 'rm -rf -- "$smoke_dir"' EXIT
cat >"$smoke_dir/smoke.c" <<'EOF'
#include <iniparser/dictionary.h>
#include <iniparser/iniparser.h>

#include <string.h>

int main(void) {
    dictionary *config = dictionary_new(0);
    if (config == NULL) {
        return 1;
    }
    if (iniparser_set(config, "target", NULL) != 0 ||
        iniparser_set(config, "target:isa", "RVA23") != 0) {
        dictionary_del(config);
        return 1;
    }
    const char *isa = iniparser_getstring(config, "target:isa", "missing");
    const int result = strcmp(isa, "RVA23") == 0 ? 0 : 1;
    dictionary_del(config);
    return result;
}
EOF
cc "$smoke_dir/smoke.c" $(pkg-config --cflags --libs iniparser) -o "$smoke_dir/smoke"
"$smoke_dir/smoke"
