#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- libffi libffi-devel
smoke_dir=$(mktemp -d)
trap 'rm -rf "$smoke_dir"' EXIT
cat >"$smoke_dir/smoke.c" <<'EOF'
#include <ffi.h>
static int add(int a, int b) { return a + b; }
int main(void) {
    ffi_cif cif;
    ffi_type *args[2] = {&ffi_type_sint, &ffi_type_sint};
    int a = 19, b = 23, result = 0;
    void *values[2] = {&a, &b};
    if (ffi_prep_cif(&cif, FFI_DEFAULT_ABI, 2, &ffi_type_sint, args) != FFI_OK) return 1;
    ffi_call(&cif, FFI_FN(add), &result, values);
    return result == 42 ? 0 : 2;
}
EOF
cc "$smoke_dir/smoke.c" -lffi -o "$smoke_dir/smoke"
"$smoke_dir/smoke"
