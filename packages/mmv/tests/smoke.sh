#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- mmv
mmv --version
smoke_dir=$(mktemp -d)
trap 'rm -rf "$smoke_dir"' EXIT
(
  cd "$smoke_dir"
  printf 'installed wildcard move\n' > before.txt
  mmv 'before.*' 'after.#1'
  test ! -e before.txt
  test "$(cat after.txt)" = 'installed wildcard move'
  mcp 'after.*' 'copy.#1'
  cmp after.txt copy.txt
)
