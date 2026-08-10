#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- libzip libzip-devel
smoke_dir=$(mktemp -d)
trap 'rm -rf "$smoke_dir"' EXIT
cat >"$smoke_dir/smoke.c" <<'EOF'
#include <zip.h>
int main(int argc, char **argv) {
    int error = 0;
    zip_t *archive = zip_open(argv[1], ZIP_CREATE | ZIP_TRUNCATE, &error);
    if (archive == 0) return 1;
    return zip_close(archive) == 0 ? 0 : 2;
}
EOF
cc "$smoke_dir/smoke.c" -lzip -o "$smoke_dir/smoke"
"$smoke_dir/smoke" "$smoke_dir/smoke.zip"
test -s "$smoke_dir/smoke.zip"
