#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- xmlstarlet xmlstarlet-help
xmlstarlet --version | sed -n '1p' | grep -Fx '1.6.1'

smoke_dir=$(mktemp -d)
trap 'rm -rf "$smoke_dir"' EXIT
cat >"$smoke_dir/input.xml" <<'EOF'
<root><value>RVA23</value></root>
EOF
xmlstarlet sel -t -v '/root/value' -n "$smoke_dir/input.xml" \
  | grep -Fx 'RVA23'
xmlstarlet fo "$smoke_dir/input.xml" >"$smoke_dir/formatted.xml"
grep -F '<value>RVA23</value>' "$smoke_dir/formatted.xml"
