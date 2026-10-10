#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- entr
d=$(mktemp -d); trap 'rm -rf "$d"' EXIT
touch "$d/watch"
(sleep 1; printf x >>"$d/watch") &
printf '%s\n' "$d/watch" | timeout 10 entr -p sh -c 'test -s "$0"' "$d/watch"
