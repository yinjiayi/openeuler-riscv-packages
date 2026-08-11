#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- gzip
gzip --version | grep -F 'gzip 1.14'

smoke_dir=$(mktemp -d)
trap 'rm -rf "$smoke_dir"' EXIT
printf 'openEuler riscv64 RVA23\n' >"$smoke_dir/input"
gzip -c "$smoke_dir/input" >"$smoke_dir/input.gz"
gzip -t "$smoke_dir/input.gz"
gzip -dc "$smoke_dir/input.gz" >"$smoke_dir/output"
cmp "$smoke_dir/input" "$smoke_dir/output"
zgrep -F 'riscv64 RVA23' "$smoke_dir/input.gz"
