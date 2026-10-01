#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- wavpack wavpack-devel

smoke_dir=$(mktemp -d)
trap 'rm -rf "$smoke_dir"' EXIT

{
  printf 'RIFF\054\000\000\000WAVEfmt \020\000\000\000\001\000\001\000'
  printf '\100\037\000\000\100\037\000\000\001\000\010\000data\010\000\000\000'
  printf '\000\040\100\140\200\240\300\340'
} >"$smoke_dir/input.wav"
printf '\000\040\100\140\200\240\300\340' >"$smoke_dir/expected.raw"

wavpack -q "$smoke_dir/input.wav" -o "$smoke_dir/sample.wv"
wvunpack -q -r "$smoke_dir/sample.wv" -o "$smoke_dir/decoded.raw"
cmp "$smoke_dir/expected.raw" "$smoke_dir/decoded.raw"

cat >"$smoke_dir/smoke.c" <<'EOF'
#include <wavpack/wavpack.h>

#include <string.h>

int main(void) {
    return strcmp(WavpackGetLibraryVersionString(), "5.9.0") != 0;
}
EOF

read -r -a pc_flags <<<"$(pkg-config --cflags --libs wavpack)"
cc "$smoke_dir/smoke.c" "${pc_flags[@]}" -o "$smoke_dir/smoke"
"$smoke_dir/smoke"
