#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

command -v lsdiff >/dev/null
command -v filterdiff >/dev/null
tmpdir="$(mktemp -d)"
trap 'rm -rf -- "$tmpdir"' EXIT
cat >"$tmpdir/change.patch" <<'EOF'
--- a/one.txt
+++ b/one.txt
@@ -1 +1 @@
-old
+new
--- a/two.txt
+++ b/two.txt
@@ -1 +1 @@
-left
+right
EOF
lsdiff "$tmpdir/change.patch" | grep -Fx 'a/one.txt'
filterdiff -i '*/two.txt' "$tmpdir/change.patch" | grep -F '+right'
