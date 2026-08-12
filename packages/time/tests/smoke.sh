#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- time
/usr/bin/time --version | head -n 1 | grep -F 'GNU time 1.10'

smoke_dir=$(mktemp -d)
trap 'rm -rf "$smoke_dir"' EXIT
/usr/bin/time -f '%x' -o "$smoke_dir/status" sh -c 'exit 0'
grep -Fx '0' "$smoke_dir/status"
