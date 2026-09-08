#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- jpeginfo
jpeginfo --version | grep -F 'jpeginfo v1.7.1'

smoke_dir=$(mktemp -d)
trap 'rm -rf "$smoke_dir"' EXIT
printf 'not a JPEG\n' >"$smoke_dir/corrupt.jpg"
if jpeginfo -c "$smoke_dir/corrupt.jpg" >"$smoke_dir/result" 2>&1; then
  echo "jpeginfo unexpectedly accepted corrupt input" >&2
  exit 1
fi
grep -E 'ERROR[[:space:]]+Not a JPEG file' "$smoke_dir/result"
