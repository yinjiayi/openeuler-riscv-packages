#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- ed
ed --version | grep -F 'GNU ed'

smoke_dir=$(mktemp -d)
trap 'rm -rf "$smoke_dir"' EXIT
printf 'alpha\n' >"$smoke_dir/document"
printf 'a\nbeta\n.\nw\nq\n' | ed -s "$smoke_dir/document"
printf 'alpha\nbeta\n' >"$smoke_dir/expected"
cmp "$smoke_dir/expected" "$smoke_dir/document"
