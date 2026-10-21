#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- libarchive libarchive-devel libarchive-help bsdtar bsdcpio bsdcat bsdunzip

for tool in bsdtar bsdcpio bsdcat bsdunzip; do
  "$tool" --version | grep -F -- '3.8.9' >/dev/null
done

smoke_dir=$(mktemp -d)
trap 'rm -rf "$smoke_dir"' EXIT

printf '%s\n' 'libarchive RVA23 smoke' >"$smoke_dir/input.txt"
bsdtar -cf "$smoke_dir/smoke.tar" -C "$smoke_dir" input.txt
mkdir "$smoke_dir/output"
bsdtar -xf "$smoke_dir/smoke.tar" -C "$smoke_dir/output"
cmp "$smoke_dir/input.txt" "$smoke_dir/output/input.txt"

cat >"$smoke_dir/smoke.c" <<'EOF'
#include <archive.h>
#include <string.h>

int main(void) {
    return strstr(archive_version_string(), "libarchive 3.8.9") ? 0 : 1;
}
EOF

cc "$smoke_dir/smoke.c" -larchive -o "$smoke_dir/smoke"
"$smoke_dir/smoke"
