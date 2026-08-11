#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- libhangul libhangul-devel
task_dir=$(mktemp -d)
trap 'rm -rf -- "$task_dir"' EXIT
cat >"$task_dir/smoke.c" <<'C'
#include <hangul.h>
int main(void) {
  HangulInputContext *context = hangul_ic_new("2");
  if (!context) return 1;
  hangul_ic_delete(context);
  return 0;
}
C
gcc "$task_dir/smoke.c" -I/usr/include/hangul-1.0 -lhangul -o "$task_dir/smoke"
"$task_dir/smoke"
