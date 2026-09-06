#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- goocanvas2 goocanvas2-devel python3-goocanvas2
rpm -q --whatprovides 'pkgconfig(goocanvas-2.0)'
test "$(pkg-config --modversion goocanvas-2.0)" = '2.0.4'

tmpdir="$(mktemp -d)"
trap 'rm -rf -- "$tmpdir"' EXIT
cat >"$tmpdir/check.c" <<'EOF'
#include <goocanvas.h>
#include <glib-object.h>
int main(void) {
  GType canvas_type = goo_canvas_get_type();
  return canvas_type == G_TYPE_INVALID ? 1 : 0;
}
EOF
read -r -a goocanvas_cflags <<<"$(pkg-config --cflags goocanvas-2.0)"
read -r -a goocanvas_libs <<<"$(pkg-config --libs goocanvas-2.0)"
cc "$tmpdir/check.c" "${goocanvas_cflags[@]}" "${goocanvas_libs[@]}" -o "$tmpdir/check"
"$tmpdir/check"

python3 - <<'PY'
import gi
gi.require_version("GooCanvas", "2.0")
from gi.repository import GooCanvas
assert GooCanvas.Canvas.__gtype__.name == "GooCanvas"
PY
