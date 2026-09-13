#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- cloc
cloc --version | grep -F "2.10"
smoke_dir=$(mktemp -d)
trap 'rm -rf -- "$smoke_dir"' EXIT
printf "%s\n" "#include <stdio.h>" "int main(void) { return 0; }" >"$smoke_dir/main.c"
cloc --quiet --json --out="$smoke_dir/count.json" "$smoke_dir"
grep -F '"C"' "$smoke_dir/count.json"
