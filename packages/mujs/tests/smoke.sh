#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- mujs mujs-devel
test "$(pkg-config --modversion mujs)" = "1.3.10"

smoke_dir=$(mktemp -d)
trap 'rm -rf -- "$smoke_dir"' EXIT
cat >"$smoke_dir/runtime.js" <<'EOF'
var values = JSON.parse('[2,3,5]');
if (values[0] + values[1] + values[2] !== 10)
    throw new Error('unexpected JavaScript result');
print('installed-mujs-ok');
EOF
mujs "$smoke_dir/runtime.js" | grep -Fx 'installed-mujs-ok'
mujs-pp "$smoke_dir/runtime.js" > "$smoke_dir/pretty.js"
mujs "$smoke_dir/pretty.js" | grep -Fx 'installed-mujs-ok'

cat >"$smoke_dir/embedding.c" <<'EOF'
#include <mujs.h>

int main(void) {
    js_State *state = js_newstate(0, 0, 0);
    int result;
    if (state == 0) return 1;
    result = js_dostring(state, "var answer = 6 * 7;");
    if (result == 0) {
        js_getglobal(state, "answer");
        result = js_tonumber(state, -1) == 42 ? 0 : 2;
        js_pop(state, 1);
    }
    js_freestate(state);
    return result;
}
EOF
read -r -a mujs_flags <<< "$(pkg-config --cflags --libs mujs)"
cc "$smoke_dir/embedding.c" "${mujs_flags[@]}" -o "$smoke_dir/embedding"
"$smoke_dir/embedding"
