#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- uriparser uriparser-devel

smoke_dir=$(mktemp -d)
trap 'rm -rf "$smoke_dir"' EXIT

uriparse 'https://example.com/riscv64?isa=RVA23' >"$smoke_dir/uriparse.out"
grep -Eq '^scheme:[[:space:]]+https$' "$smoke_dir/uriparse.out"
grep -Eq '^hostText:[[:space:]]+example\.com$' "$smoke_dir/uriparse.out"

cat >"$smoke_dir/smoke.c" <<'EOF'
#include <uriparser/Uri.h>
#include <stddef.h>

int main(void) {
    static const char input[] = "https://example.com/riscv64?isa=RVA23";
    UriParserStateA state;
    UriUriA uri;
    ptrdiff_t scheme_length;
    state.uri = &uri;
    if (uriParseUriA(&state, input) != URI_SUCCESS)
        return 1;
    scheme_length = uri.scheme.afterLast - uri.scheme.first;
    if (scheme_length != 5 || uri.hostText.first == NULL) {
        uriFreeUriMembersA(&uri);
        return 2;
    }
    uriFreeUriMembersA(&uri);
    return 0;
}
EOF

cc "$smoke_dir/smoke.c" $(pkg-config --cflags --libs liburiparser) -o "$smoke_dir/smoke"
"$smoke_dir/smoke"
