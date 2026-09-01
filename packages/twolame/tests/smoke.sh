#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- twolame twolame-devel
d=$(mktemp -d); trap 'rm -rf "$d"' EXIT
printf '#include <twolame.h>\nint main(void){twolame_options*o=twolame_init();if(!o)return 1;twolame_close(&o);return 0;}\n' >"$d/a.c"
gcc "$d/a.c" -o "$d/a" $(pkg-config --cflags --libs twolame)
"$d/a"
