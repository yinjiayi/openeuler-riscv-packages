#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- indent
indent --version | head -n1 | grep -F 'GNU indent 2.2.13'
d=$(mktemp -d); trap 'rm -rf "$d"' EXIT
printf '%s\n' 'int main(void){return 0;}' >"$d/in.c"
indent -gnu -st <"$d/in.c" >"$d/out.c"
grep -F 'int main (void)' "$d/out.c"
cc -Wall -Werror "$d/out.c" -o "$d/out"
"$d/out"
