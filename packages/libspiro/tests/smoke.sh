#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- libspiro libspiro-devel
task_dir=$(mktemp -d)
trap 'rm -rf -- "$task_dir"' EXIT
cat >"$task_dir/smoke.c" <<'C'
#include <spiro.h>
int main(void) {
  return run_spiro != 0 ? 0 : 1;
}
C
gcc "$task_dir/smoke.c" -lspiro -o "$task_dir/smoke"
"$task_dir/smoke"
