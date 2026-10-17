#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- global
test "$(global -q --version)" = 6.7
d=$(mktemp -d); trap 'rm -rf "$d"' EXIT
cat >"$d/main.c" <<'EOF'
static int answer(void) { return 42; }
int main(void) { return answer() == 42 ? 0 : 1; }
EOF
(cd "$d" && gtags && test -s GPATH && test -s GRTAGS && test -s GTAGS && global -x answer | grep -F 'main.c')
