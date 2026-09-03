#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- time
test "$(/usr/bin/time --version | sed -n '1s/.* //p')" = 1.10

smoke_dir=$(mktemp -d)
trap 'rm -rf "$smoke_dir"' EXIT
/usr/bin/time -f '%x' -o "$smoke_dir/status" sh -c 'exit 0'
grep -Fx '0' "$smoke_dir/status"
