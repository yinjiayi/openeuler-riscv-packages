#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- libdeflate libdeflate-devel
task_dir=$(mktemp -d)
trap 'rm -rf -- "$task_dir"' EXIT
printf '%s\n' 'openEuler RISC-V libdeflate smoke test' >"$task_dir/input.txt"
libdeflate-gzip -c "$task_dir/input.txt" >"$task_dir/input.gz"
libdeflate-gunzip -c "$task_dir/input.gz" >"$task_dir/output.txt"
cmp -- "$task_dir/input.txt" "$task_dir/output.txt"
