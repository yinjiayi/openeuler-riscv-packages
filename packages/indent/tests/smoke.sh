#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- indent
set +e
version_output=$(indent --version 2>&1)
version_status=$?
set -e
test "$version_status" -eq 64
printf '%s\n' "$version_output" | grep -Fx 'GNU indent 2.2.13'
d=$(mktemp -d); trap 'rm -rf "$d"' EXIT
printf '%s\n' 'int main(void){return 0;}' >"$d/in.c"
indent -gnu -st <"$d/in.c" >"$d/out.c"
grep -Fx 'int' "$d/out.c"
grep -Fx 'main (void)' "$d/out.c"
cc -Wall -Werror "$d/out.c" -o "$d/out"
"$d/out"
