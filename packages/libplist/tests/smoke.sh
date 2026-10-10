#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- libplist libplist-devel
test "$(pkg-config --modversion libplist-2.0)" = "2.7.0"
test "$(pkg-config --modversion libplist++-2.0)" = "2.7.0"
plistutil --version | grep -F '2.7.0'

smoke_dir=$(mktemp -d)
trap 'rm -rf -- "$smoke_dir"' EXIT
cat >"$smoke_dir/input.json" <<'EOF'
{"arch":"riscv64","isa":"RVA23"}
EOF
plistutil --infile "$smoke_dir/input.json" --outfile "$smoke_dir/output.bplist" --format bin
plistutil --infile "$smoke_dir/output.bplist" --outfile "$smoke_dir/roundtrip.json" --format json
grep -F '"arch"' "$smoke_dir/roundtrip.json"
grep -F '"riscv64"' "$smoke_dir/roundtrip.json"
grep -F '"RVA23"' "$smoke_dir/roundtrip.json"

cat >"$smoke_dir/embedding.c" <<'EOF'
#include <plist/plist.h>
#include <stdlib.h>
#include <string.h>

int main(void) {
    plist_t root = plist_new_dict();
    char *arch = NULL;
    int result;
    if (root == NULL) return 1;
    plist_dict_set_item(root, "arch", plist_new_string("riscv64"));
    plist_get_string_val(plist_dict_get_item(root, "arch"), &arch);
    result = arch != NULL && strcmp(arch, "riscv64") == 0 ? 0 : 2;
    free(arch);
    plist_free(root);
    return result;
}
EOF
read -r -a plist_flags <<< "$(pkg-config --cflags --libs libplist-2.0)"
cc "$smoke_dir/embedding.c" "${plist_flags[@]}" -o "$smoke_dir/embedding"
"$smoke_dir/embedding"
