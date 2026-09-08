#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- libuv libuv-devel
task_dir=$(mktemp -d)
trap 'rm -rf -- "$task_dir"' EXIT
cat >"$task_dir/smoke.c" <<'C'
#include <string.h>
#include <uv.h>
int main(void) {
  return strcmp(uv_version_string(), "1.52.1") == 0 ? 0 : 1;
}
C
gcc "$task_dir/smoke.c" -luv -pthread -ldl -lrt -o "$task_dir/smoke"
"$task_dir/smoke"
