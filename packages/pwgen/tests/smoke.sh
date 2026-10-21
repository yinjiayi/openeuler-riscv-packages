#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- pwgen
smoke_dir=$(mktemp -d)
trap 'rm -rf "$smoke_dir"' EXIT

pwgen -s -1 20 5 >"$smoke_dir/passwords"
awk 'length($0) != 20 { exit 1 } END { if (NR != 5) exit 1 }' \
  "$smoke_dir/passwords"
