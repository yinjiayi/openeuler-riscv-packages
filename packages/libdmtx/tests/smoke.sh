#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- libdmtx libdmtx-devel
task_dir=$(mktemp -d)
trap 'rm -rf -- "$task_dir"' EXIT
cat >"$task_dir/smoke.c" <<'C'
#include <dmtx.h>
#include <string.h>
int main(void) {
  const char *version = dmtxVersion();
  return version != 0 && strcmp(version, "0.7.8") == 0 ? 0 : 1;
}
C
gcc "$task_dir/smoke.c" -ldmtx -o "$task_dir/smoke"
"$task_dir/smoke"
