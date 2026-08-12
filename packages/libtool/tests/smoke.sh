#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- libtool libtool-ltdl libtool-ltdl-devel
libtool --version | head -n 1 | grep -Fx 'libtool (GNU libtool) 2.6.2'

smoke_dir=$(mktemp -d)
trap 'rm -rf "$smoke_dir"' EXIT
cat >"$smoke_dir/answer.c" <<'EOF'
int libtool_answer(void) { return 42; }
EOF
cat >"$smoke_dir/main.c" <<'EOF'
#include <ltdl.h>
extern int libtool_answer(void);
int main(void) {
    if (lt_dlinit() != 0)
        return 1;
    if (lt_dlexit() != 0)
        return 2;
    return libtool_answer() == 42 ? 0 : 3;
}
EOF
cd "$smoke_dir"
libtool --mode=compile --quiet cc -c answer.c -o answer.lo
libtool --mode=link --quiet cc -rpath "$smoke_dir/lib" -o libanswer.la answer.lo
libtool --mode=link --quiet cc -o smoke main.c libanswer.la -lltdl
libtool --mode=execute ./smoke
