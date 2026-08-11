#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- patch
patch --version | head -n 1 | grep -Fx 'GNU patch 2.8'
smoke_dir=$(mktemp -d)
trap 'rm -rf "$smoke_dir"' EXIT

cat >"$smoke_dir/message.txt" <<'EOF'
openEuler
riscv64
EOF
cat >"$smoke_dir/change.diff" <<'EOF'
--- message.txt
+++ message.txt
@@ -1,2 +1,3 @@
 openEuler
 riscv64
+RVA23
EOF

(
  cd "$smoke_dir"
  patch --batch --forward message.txt <change.diff
)
grep -Fx 'RVA23' "$smoke_dir/message.txt"
