#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- re2c
re2c --version | grep -Fx 're2c 4.5.1'
tmpdir="$(mktemp -d)"
trap 'rm -rf -- "$tmpdir"' EXIT
cat >"$tmpdir/fixture.re" <<'EOF'
typedef unsigned char YYCTYPE;
static int scan(const YYCTYPE *YYCURSOR) {
    const YYCTYPE *YYMARKER;
    /*!re2c
        re2c:yyfill:enable = 0;
        "RVA23" { return 0; }
        * { return 1; }
    */
}
int main(void) { static const YYCTYPE input[] = "RVA23"; return scan(input); }
EOF
re2c -o "$tmpdir/fixture.c" "$tmpdir/fixture.re"
cc "$tmpdir/fixture.c" -o "$tmpdir/fixture"
"$tmpdir/fixture"
