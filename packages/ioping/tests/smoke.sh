#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- ioping
test "$(ioping -v)" = "ioping 1.3"
smoke_dir=$(mktemp -d)
trap 'rm -rf -- "$smoke_dir"' EXIT

result=$(LC_ALL=C ioping -i 10ms -c 3 -s 512 -S 16k "$smoke_dir")
grep -Fq 'generated 3 requests' <<<"$result"
