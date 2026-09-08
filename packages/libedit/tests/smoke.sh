#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- libedit libedit-devel

smoke_dir=$(mktemp -d)
trap 'rm -rf "$smoke_dir"' EXIT

cat >"$smoke_dir/smoke.c" <<'EOF'
#include <histedit.h>
#include <stdio.h>

int main(void) {
  EditLine *editor = el_init("libedit-smoke", stdin, stdout, stderr);
  if (editor == NULL) {
    return 1;
  }
  el_end(editor);
  return 0;
}
EOF

cc -Wall -Werror "$smoke_dir/smoke.c" -o "$smoke_dir/smoke" -ledit
TERM=dumb "$smoke_dir/smoke" </dev/null
