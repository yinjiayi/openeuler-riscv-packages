#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- unrtf

smoke_dir=$(mktemp -d)
trap 'rm -rf -- "$smoke_dir"' EXIT
printf '%s\n' '{\rtf1\ansi\deff0{\fonttbl{\f0\fnil Arial;}}\f0 PlainMarker \b BoldMarker\b0\par}' > "$smoke_dir/input.rtf"

(
  cd "$smoke_dir"
  unrtf --html input.rtf > html.out
  unrtf --text input.rtf > text.out
)

grep -Fq '<html>' "$smoke_dir/html.out"
grep -Fq '<b>' "$smoke_dir/html.out"
grep -Fq '</b>' "$smoke_dir/html.out"
grep -Fq 'PlainMarker' "$smoke_dir/html.out"
grep -Fq 'BoldMarker' "$smoke_dir/html.out"
grep -Fq 'PlainMarker' "$smoke_dir/text.out"
grep -Fq 'BoldMarker' "$smoke_dir/text.out"
if grep -Fq '<html>' "$smoke_dir/text.out"; then
  exit 1
fi
if grep -Fq '\rtf1' "$smoke_dir/text.out"; then
  exit 1
fi
