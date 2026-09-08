#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- libb2 libb2-devel
task_dir=$(mktemp -d)
trap 'rm -rf -- "$task_dir"' EXIT
cat >"$task_dir/smoke.c" <<'C'
#include <blake2.h>
#include <stdint.h>
int main(void) {
  uint8_t out[64] = {0};
  return blake2b(out, "abc", 0, sizeof(out), 3, 0) == 0 && out[0] != 0 ? 0 : 1;
}
C
gcc "$task_dir/smoke.c" -lb2 -o "$task_dir/smoke"
"$task_dir/smoke"
