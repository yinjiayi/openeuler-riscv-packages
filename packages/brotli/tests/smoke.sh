#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- brotli brotli-devel
task_dir=$(mktemp -d)
trap 'rm -rf -- "$task_dir"' EXIT
printf '%s\n' 'openEuler RISC-V Brotli smoke test' >"$task_dir/input.txt"
brotli --force --quality=5 --output="$task_dir/input.br" "$task_dir/input.txt"
brotli --force --decompress --output="$task_dir/output.txt" "$task_dir/input.br"
cmp -- "$task_dir/input.txt" "$task_dir/output.txt"
